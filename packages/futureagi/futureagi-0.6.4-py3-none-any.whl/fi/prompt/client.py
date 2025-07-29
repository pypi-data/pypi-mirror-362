import time
from typing import Dict, Optional

from fi.api.auth import APIKeyAuth, ResponseHandler
from fi.api.types import HttpMethod, RequestConfig
from fi.prompt.types import ModelConfig, PromptTemplate
from fi.utils.errors import InvalidAuthError, SDKException, TemplateAlreadyExists
from fi.utils.errors import TemplateNotFound
from fi.utils.logging import logger
from fi.utils.routes import Routes


class SimpleJsonResponseHandler(ResponseHandler[Dict, Dict]):
    """Simply parses JSON and handles common errors."""

    @classmethod
    def _parse_success(cls, response) -> Dict:
        return response.json()

    @classmethod
    def _handle_error(cls, response) -> None:
        if response.status_code == 403:
            raise InvalidAuthError()
        if response.status_code == 404:
            raise TemplateNotFound("Could not find template during polling.")
        else:
            try:
                detail = response.json()
                raise SDKException(
                    f"Polling failed: {detail.get('message', response.text)}"
                )
            except Exception:
                response.raise_for_status()


class PromptResponseHandler(ResponseHandler[Dict, PromptTemplate]):
    """Handles responses for prompt requests"""

    @classmethod
    def _parse_success(cls, response) -> Dict:
        """Handles responses for prompt requests"""
        data = response.json()

        # Handle search endpoint
        if "search=" in response.url:
            results = data.get("results", [])
            name = response.url.split("search=")[1]
            for item in results:
                if item["name"] == name:
                    return item["id"]
            raise ValueError(f"No template found with the given name: {name}")

        # Handle GET template by ID endpoint
        if response.request.method == HttpMethod.GET.value:
            prompt_config_raw = data.get("promptConfig", [{}])[0]
            cfg_src = prompt_config_raw.get("configuration", {})
            cfg = {
                "modelName": cfg_src.get("modelName") or cfg_src.get("model"),
                "temperature": cfg_src.get("temperature"),
                "frequencyPenalty": cfg_src.get("frequencyPenalty") or cfg_src.get("frequency_penalty"),
                "presencePenalty": cfg_src.get("presencePenalty") or cfg_src.get("presence_penalty"),
                "maxTokens": cfg_src.get("maxTokens") or cfg_src.get("max_tokens"),
                "topP": cfg_src.get("topP") or cfg_src.get("top_p"),
                "responseFormat": cfg_src.get("responseFormat") or cfg_src.get("response_format"),
                "toolChoice": cfg_src.get("toolChoice") or cfg_src.get("tool_choice"),
                "tools": cfg_src.get("tools"),
            }
            model_config = ModelConfig(
                model_name=cfg["modelName"] or "unavailable",
                temperature=cfg["temperature"] if cfg["temperature"] is not None else 0,
                frequency_penalty=cfg["frequencyPenalty"] if cfg["frequencyPenalty"] is not None else 0,
                presence_penalty=cfg["presencePenalty"] if cfg["presencePenalty"] is not None else 0,
                max_tokens=cfg["maxTokens"],
                top_p=cfg["topP"] if cfg["topP"] is not None else 0,
                response_format=cfg["responseFormat"],
                tool_choice=cfg["toolChoice"],
                tools=cfg["tools"],
            )
            template_data = {
                "id": data.get("id"),
                "name": data.get("name"),
                "description": data.get("description", ""),
                "messages": prompt_config_raw.get("messages", []),
                "model_configuration": model_config,
                "variable_names": data.get("variableNames", {}),
                "version": data.get("version"),
                "is_default": data.get("isDefault", True),
                "evaluation_configs": data.get("evaluationConfigs", []),
                "status": data.get("status"),
                "error_message": data.get("errorMessage"),
            }
            return PromptTemplate(**template_data)

        if response.request.method == HttpMethod.POST.value and response.url.endswith(
            Routes.create_template.value
        ):
            return data["result"]

        # Return raw data for other endpoints
        return data

    @classmethod
    def _handle_error(cls, response) -> None:
        if response.status_code == 403:
            raise InvalidAuthError()
        if response.status_code == 404:
            # Attempt to extract 'name' query param for better message
            import urllib.parse as _up

            parsed = _up.urlparse(response.request.url)
            qs = _up.parse_qs(parsed.query)
            name_param = qs.get("name", [None])[0]
            raise TemplateNotFound(name_param or "unknown")
        if response.status_code == 400:
            try:
                detail = response.json()
                error_code = detail.get("errorCode") if isinstance(detail, dict) else None
            except Exception:
                error_code = None

            if error_code == "TEMPLATE_ALREADY_EXIST":
                raise TemplateAlreadyExists(detail.get("name", "<unknown>"))
            raise SDKException(
                detail.get("message", "Bad request – please verify request body."))
        else:
            response.raise_for_status()


class Prompt(APIKeyAuth):
    _template_id_cache = {}

    @staticmethod
    def _dict_to_prompt_template(item: Dict) -> PromptTemplate:
        """Safely convert backend JSON to PromptTemplate."""

        prompt_config_raw = item.get("promptConfig") or item.get("prompt_config")

        if prompt_config_raw:
            pc = prompt_config_raw[0] if isinstance(prompt_config_raw, list) else prompt_config_raw
            cfg_raw = pc.get("configuration", {})
            # Normalize key casing / naming
            cfg = {
                "modelName": cfg_raw.get("modelName") or cfg_raw.get("model"),
                "temperature": cfg_raw.get("temperature"),
                "frequencyPenalty": cfg_raw.get("frequencyPenalty") or cfg_raw.get("frequency_penalty"),
                "presencePenalty": cfg_raw.get("presencePenalty") or cfg_raw.get("presence_penalty"),
                "maxTokens": cfg_raw.get("maxTokens") or cfg_raw.get("max_tokens"),
                "topP": cfg_raw.get("topP") or cfg_raw.get("top_p"),
                "responseFormat": cfg_raw.get("responseFormat") or cfg_raw.get("response_format"),
                "toolChoice": cfg_raw.get("toolChoice") or cfg_raw.get("tool_choice"),
                "tools": cfg_raw.get("tools"),
            }
            model_config = ModelConfig(
                model_name=cfg["modelName"] or "unavailable",
                temperature=cfg["temperature"] if cfg["temperature"] is not None else 0,
                frequency_penalty=cfg["frequencyPenalty"] if cfg["frequencyPenalty"] is not None else 0,
                presence_penalty=cfg["presencePenalty"] if cfg["presencePenalty"] is not None else 0,
                max_tokens=cfg["maxTokens"],
                top_p=cfg["topP"] if cfg["topP"] is not None else 0,
                response_format=cfg["responseFormat"] if cfg["responseFormat"] is not None else None,
                tool_choice=cfg["toolChoice"] if cfg["toolChoice"] is not None else None,
                tools=cfg["tools"] if cfg["tools"] is not None else None,
            )
            messages = pc.get("messages", [])
        else:
            # Backend list endpoint doesn't include promptConfig; leave these
            # attributes unset so we don't mislead users with fake defaults.
            model_config = None
            messages = None

        return PromptTemplate(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description", ""),
            messages=messages or [],
            model_configuration=model_config or ModelConfig(),
            variable_names=item.get("variableNames") or item.get("variable_names", {}),
            version=item.get("version"),
            is_default=item.get("isDefault", True),
            evaluation_configs=item.get("evaluationConfigs", []),
            status=item.get("status"),
            error_message=item.get("errorMessage"),
        )

    @classmethod
    def list_templates(
        cls,
        fi_api_key: Optional[str] = None,
        fi_secret_key: Optional[str] = None,
        fi_base_url: Optional[str] = None,
    ) -> Dict:
        """Return the raw JSON payload from GET /model-hub/prompt-templates/.
        """

        auth_client = APIKeyAuth(
            fi_api_key=fi_api_key,
            fi_secret_key=fi_secret_key,
            fi_base_url=fi_base_url,
        )

        response = auth_client.request(
            config=RequestConfig(
                method=HttpMethod.GET,
                url=auth_client._base_url + "/" + Routes.list_templates.value,
            )
        )

        data = response.json()

        auth_client.close()

        return data

    def __init__(
        self,
        template: Optional[PromptTemplate] = None,
        fi_api_key: Optional[str] = None,
        fi_secret_key: Optional[str] = None,
        fi_base_url: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            fi_api_key=fi_api_key,
            fi_secret_key=fi_secret_key,
            fi_base_url=fi_base_url,
            **kwargs,
        )

        if template and not template.id:
            try:
                self.template = self._fetch_template_by_name(template.name)
            except Exception as e:
                logger.warning(
                    "Template not found in the backend. Create a new template before running."
                )
                self.template = template
        else:
            self.template = template
            if self.template:
                logger.warning(
                    f"Current template: {self.template.name} does not exist in the backend. Please create it first before running."
                )
            else:
                logger.warning(
                    "No template provided. Please provide a template before running."
                )

    def generate(self, requirements: str) -> "Prompt":
        """Generate a prompt and return self for chaining"""
        if not self.template:
            raise ValueError("No template configured")
        response = self.request(
            config=RequestConfig(
                method=HttpMethod.POST,
                url=self._base_url + "/" + Routes.generate_prompt.value,
                json={"statement": requirements},
            ),
            response_handler=PromptResponseHandler,
        )
        self.template.messages[-1].content = response["result"]["prompt"]
        return self

    def improve(self, requirements: str) -> "Prompt":
        """Improve prompt and return self for chaining"""
        if not self.template:
            raise ValueError("No template configured")

        existing_prompt = (
            self.template.messages[-1].content if self.template.messages else ""
        )

        improved_response = self.request(
            config=RequestConfig(
                method=HttpMethod.POST,
                url=self._base_url + "/" + Routes.improve_prompt.value,
                json={
                    "existing_prompt": existing_prompt,
                    "improvement_requirements": requirements,
                },
            ),
            response_handler=PromptResponseHandler,
        )
        self.template.messages[-1].content = improved_response["result"]["prompt"]
        return self

    def create(self) -> "Prompt":
        """Create a draft prompt template and return self for chaining"""
        if not self.template:
            raise ValueError("template must be set")

        if self.template.id:
            raise TemplateAlreadyExists(self.template.name)

        method = HttpMethod.POST
        url = self._base_url + "/" + Routes.create_template.value

        messages = []
        for message in self.template.messages:
            message_dict = message.model_dump()
            if isinstance(message_dict.get("content"), str):
                message_dict["content"] = [
                    {"type": "text", "text": message_dict["content"]}
                ]
            messages.append(message_dict)

        json = {
            "name": self.template.name,
            "prompt_config": [
                {
                    "messages": messages,
                    "configuration": {
                        "model": self.template.model_configuration.model_name,
                        "temperature": self.template.model_configuration.temperature,
                        "max_tokens": self.template.model_configuration.max_tokens,
                        "top_p": self.template.model_configuration.top_p,
                        "frequency_penalty": self.template.model_configuration.frequency_penalty,
                        "presence_penalty": self.template.model_configuration.presence_penalty,
                    },
                }
            ],
            "variable_names": self.template.variable_names,
            "evaluation_configs": self.template.evaluation_configs or [],
        }

        response = self.request(
            config=RequestConfig(
                method=method,
                url=url,
                json=json,
            ),
            response_handler=PromptResponseHandler,
        )

        self.template.id = response["id"]
        self.template.name = response["name"]
        self.template.version = response.get("templateVersion") or response.get("createdVersion") or "v1"
        return self

    def _create_new_draft(self) -> None:
        """
        Calls the internal add-new-draft endpoint to create a new version
        and updates the client's state with the new version number.
        """
        if not self.template or not self.template.id:
            raise ValueError("Template must be created before creating a new version.")

        url = (
            self._base_url
            + "/"
            + Routes.add_new_draft.value.format(template_id=self.template.id)
        )

        messages = []
        for message in self.template.messages:
            message_dict = message.model_dump()
            if isinstance(message_dict.get("content"), str):
                message_dict["content"] = [
                    {"type": "text", "text": message_dict["content"]}
                ]
            messages.append(message_dict)

        model_config = {
            "model": self.template.model_configuration.model_name,
            "temperature": self.template.model_configuration.temperature,
            "max_tokens": self.template.model_configuration.max_tokens,
            "top_p": self.template.model_configuration.top_p,
            "frequency_penalty": self.template.model_configuration.frequency_penalty,
            "presence_penalty": self.template.model_configuration.presence_penalty,
        }

        body = {
            "new_prompts": [
                {
                    "prompt_config": [
                        {"messages": messages, "configuration": model_config}
                    ],
                    "variable_names": self.template.variable_names,
                    "evaluation_configs": self.template.evaluation_configs or [],
                }
            ]
        }

        response = self.request(
            config=RequestConfig(method=HttpMethod.POST, url=url, json=body),
            response_handler=PromptResponseHandler,
        )

        if isinstance(response, dict) and response:
            result = response.get("result")
            if isinstance(result, list) and result:
                new_version_data = result[0]
                self.template.version = new_version_data.get("templateVersion")
        else:
            logger.error(
                "Failed to create new version, unexpected response format from server."
            )

    def _poll_for_result(
        self,
        version: str,
        timeout: int,
        poll_interval: int,
    ) -> Dict:
        """Poll the backend until the run completes.

        The endpoint now returns a definitive boolean ``status`` flag. We keep
        polling until that flag becomes ``True`` (or the legacy string
        ``"True"``), at which point we return a streamlined result payload.
        If an ``error_message``/``errorMessage`` appears at any point, the
        poll aborts and raises ``SDKException``.
        """
        logger.info(f"Waiting for result of version {version}...")
        start_time = time.time()

        url = (
            self._base_url
            + "/"
            + Routes.get_run_status.value.format(template_id=self.template.id)
        )
        params = {"template_version": version}


        while time.time() - start_time < timeout:
            response = self.request(
                config=RequestConfig(method=HttpMethod.GET, url=url, params=params),
                response_handler=SimpleJsonResponseHandler,
            )
            


            status_flag = response.get("status")
            execution = (response.get("result") or {}).get("executionsResult", {})
            inner_status = (response.get("result") or {}).get("status")
            output_val = execution.get("output")

            finished = (
                (status_flag is True or status_flag == "True")
                and (inner_status in ("completed", True, "True", "success", "SUCCESS"))
            )

            if finished:
                parsed_response: Dict = {
                    "status": True,
                    "result": {
                        "output": output_val,
                        "execution_id": execution.get("id"),
                        "template_version": execution.get("templateVersion"),
                        "template_name": execution.get("templateName"),
                        "original_template": execution.get("originalTemplate"),
                        "metadata": execution.get("metadata"),
                        "variable_names": execution.get("variable_names"),
                        "evaluation_results": execution.get("evaluationResults"),
                        "evaluation_configs": execution.get("evaluationConfigs"),
                    },
                }

                # Include an error message key if backend provided one (even on success).
                err_msg_on_success = (
                    response.get("error_message")
                    or response.get("errorMessage")
                    or (response.get("result", {}) or {}).get("error_message")
                    or (response.get("result", {}) or {}).get("errorMessage")
                )
                if err_msg_on_success:
                    parsed_response["error_message"] = err_msg_on_success

                return parsed_response


            error_msg = (
                response.get("error_message")
                or response.get("errorMessage")
                or (response.get("result", {}) or {}).get("error_message")
                or (response.get("result", {}) or {}).get("errorMessage")
            )

            if error_msg:
                raise SDKException(
                    f"Run failed for version {version}: {error_msg}"
                )

            # Not finished yet – wait before the next poll.
            time.sleep(poll_interval)


        raise TimeoutError(
            f"Timed out after {timeout}s waiting for result for version {version}."
        )

    def run(
        self,
        variables: Optional[Dict[str, str]] = None,
        *,
        is_run: bool = True,
        new_version: bool = False,
        prompt_config_override: Optional[list] = None,
        evaluation_configs: Optional[list] = None,
        sync: bool = True,
        timeout: int = 120,
        poll_interval: int = 2,
    ) -> Dict:
        """Run or save a prompt template version.

        Parameters
        ----------
        variables : dict | None
            Dict of variable substitutions. Each value can be a scalar or list.
        new_version : bool
            If True, create a new draft version before the run/save
        prompt_config_override : list | None
            Full prompt_config to replace the version with. Use when editing.
        is_run : bool
            True → run the template. False → only save (draft) without execution.
        evaluation_configs : list | None
            Attach/override evaluation configs for this run.
        sync : bool
            If True, wait for the async LLM call to complete.
        timeout : int
            Max seconds to wait for a result when sync=True.
        poll_interval : int
            Seconds between polling attempts when sync=True.
        """
        if not self.template:
            raise ValueError("No template configured")

        if new_version:
            self._create_new_draft()

        # validate variable names
        if variables and not self.template.variable_names:
            raise ValueError("No variable names found in template")
        
        if variables:
            for var_name in self.template.variable_names:
                if var_name not in (variables or {}):
                    raise ValueError(
                        f"Variable name {var_name} not found in variables"  # noqa: E713
                    )
        if variables is None and self.template.variable_names:
            variables = self.template.variable_names


        messages = []
        for message in self.template.messages:
            message_dict = message.model_dump()
            if isinstance(message_dict.get("content"), str):
                message_dict["content"] = [
                    {"type": "text", "text": message_dict["content"]}
                ]
            messages.append(message_dict)

        model_config = {
            "model": self.template.model_configuration.model_name,
            "temperature": self.template.model_configuration.temperature,
            "max_tokens": self.template.model_configuration.max_tokens,
            "top_p": self.template.model_configuration.top_p,
            "frequency_penalty": self.template.model_configuration.frequency_penalty,
            "presence_penalty": self.template.model_configuration.presence_penalty,
        }

        # Transform variable_names to expected format
        formatted_variables = {
            k: [v] if not isinstance(v, list) else v
            for k, v in (variables or {}).items()
        }

        # Ensure all variable arrays are of equal length
        if formatted_variables:
            lengths = [len(lst) for lst in formatted_variables.values()]
            if len(set(lengths)) > 1:
                raise ValueError(
                    f"All variables must be lists of equal length, got lengths: {lengths}"
                )

        body = {
            "is_run": "prompt" if is_run else "draft",
            "is_sdk": True,
            "version": self.template.version,
        }

        if evaluation_configs is not None:
            body["evaluation_configs"] = evaluation_configs

        # prompt_config
        if prompt_config_override is not None:
            body["prompt_config"] = prompt_config_override
        else:
            body["prompt_config"] = [
                {
                    "messages": messages,
                    "configuration": model_config,
                }
            ]

        if formatted_variables:
            body["variable_names"] = formatted_variables

        response = self.request(
            config=RequestConfig(
                method=HttpMethod.POST,
                url=self._base_url
                + "/"
                + Routes.run_template.value.format(template_id=self.template.id),
                json=body,
            ),
            response_handler=PromptResponseHandler,
        )
        self.template.version = response.get("version", self.template.version)

        if is_run and sync:
            version_to_poll = self.template.version
            if not version_to_poll:
                logger.warning(
                    "No version returned from run command, cannot poll for result."
                )
                return response

            try:
                return self._poll_for_result(
                    version=version_to_poll,
                    timeout=timeout,
                    poll_interval=poll_interval,
                )
            except Exception as e:
                logger.error(f"Failed to get run result: {e}")
                return response

        return response


    def delete(self) -> bool:
        """Delete the current template (requires `self.template.id`).

        Returns True when deletion succeeds. If the template has no `id`, a
        ValueError is raised.
        """
        if not self.template or not self.template.id:
            raise ValueError("Template ID missing; cannot delete.")

        self.request(
            config=RequestConfig(
                method=HttpMethod.DELETE,
                url=self._base_url
                + "/"
                + Routes.delete_template.value.format(template_id=self.template.id),
            ),
            response_handler=None,
        )

        # Clear local reference so user knows it's gone.
        self.template = None
        return True

    @classmethod
    def delete_template_by_name(
        cls,
        name: str,
        fi_api_key: Optional[str] = None,
        fi_secret_key: Optional[str] = None,
        fi_base_url: Optional[str] = None,
    ) -> bool:
        """Delete a template by its exact name.
        """

        client = APIKeyAuth(
            fi_api_key=fi_api_key,
            fi_secret_key=fi_secret_key,
            fi_base_url=fi_base_url,
        )

        try:
            tmpl: PromptTemplate = client.request(
                config=RequestConfig(
                    method=HttpMethod.GET,
                    url=client._base_url + "/" + Routes.get_template_by_name.value,
                    params={"name": name},
                ),
                response_handler=PromptResponseHandler,
            )

            client.request(
                config=RequestConfig(
                    method=HttpMethod.DELETE,
                    url=client._base_url
                    + "/"
                    + Routes.delete_template.value.format(template_id=tmpl.id),
                ),
                response_handler=None,
            )
            return True
        finally:
            client.close()

    # Keep existing methods but update them to work with PromptTemplate
    def _fetch_template_by_name(self, name: str) -> PromptTemplate:
        """Fetch template configuration by exact name using dedicated endpoint"""
        response = self.request(
            config=RequestConfig(
                method=HttpMethod.GET,
                url=self._base_url + "/" + Routes.get_template_by_name.value,
                params={"name": name},
            ),
            response_handler=PromptResponseHandler,
        )
        return response
    
    def _fetch_template_version_history(self):
        """Fetch template version history"""
        logger.info(f"Fetching template version history for {self.template.name}")

        response = self.request(
            config=RequestConfig(
                method=HttpMethod.GET,
                url=self._base_url + "/" + Routes.get_template_version_history.value,
                params={"template_id": self.template.id},
            )
        )

        results = response.json().get("results", [])
        if not results:
            raise ValueError(f"No template found with name: {self.template.name}")

        return results

    def _fetch_model_details(self, model_name: str):
        if not model_name:
            raise ValueError("Model name is required")
        """Fetch model details"""
        response = self.request(
            config=RequestConfig(
                method=HttpMethod.GET,
                url=self._base_url + "/" + Routes.get_model_details.value,
                params={"model_name": model_name}
            )
        )

        results = response.json().get("results", [])
        if not results:
            raise ValueError(f"No model found with name: {model_name}")

        return results[0]

    # Public convenience
    @classmethod
    def get_template_by_name(
        cls,
        name: str,
        fi_api_key: Optional[str] = None,
        fi_secret_key: Optional[str] = None,
        fi_base_url: Optional[str] = None,
    ) -> PromptTemplate:
        """Retrieve a prompt template by its exact name.

        Raises
        ------
        TemplateNotFound
            If the backend returns 404 meaning no template with that name exists.
        """

        client = APIKeyAuth(
            fi_api_key=fi_api_key,
            fi_secret_key=fi_secret_key,
            fi_base_url=fi_base_url,
        )

        try:
            template: PromptTemplate = client.request(
                config=RequestConfig(
                    method=HttpMethod.GET,
                    url=client._base_url + "/" + Routes.get_template_by_name.value,
                    params={"name": name},
                ),
                response_handler=PromptResponseHandler,
            )
            return template
        finally:
            client.close()
