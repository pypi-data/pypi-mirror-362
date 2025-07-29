import asyncio
import os
import uuid
from typing import Any, Dict, Optional, Union

import httpx


class MissingConfigError(Exception):
    def __init__(self, param: str):
        super().__init__(f"Config parameter '{param}' is missing")


class InvalidParameterError(Exception):
    pass


class UnauthorizedError(Exception):
    def __init__(self, message="Invalid or expired access token"):
        super().__init__(message)


class HivetraceSDK:
    def __init__(
        self, config: Optional[Dict[str, Any]] = None, async_mode: bool = True
    ) -> None:
        self.config = config or self._load_config_from_env()
        self.hivetrace_url = self._get_required_config("HIVETRACE_URL")
        self.hivetrace_access_token = self._get_required_config(
            "HIVETRACE_ACCESS_TOKEN"
        )
        self.async_mode = async_mode
        self.session = httpx.AsyncClient() if async_mode else httpx.Client()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.async_mode:
            self.session.close()

    def _load_config_from_env(self) -> Dict[str, Any]:
        return {
            "HIVETRACE_URL": os.getenv("HIVETRACE_URL", "").strip(),
            "HIVETRACE_ACCESS_TOKEN": os.getenv("HIVETRACE_ACCESS_TOKEN", "").strip(),
        }

    def _get_required_config(self, key: str) -> str:
        value = self.config.get(key, "").strip()
        if not value:
            raise MissingConfigError(key)
        return value.rstrip("/")

    @staticmethod
    def _validate_application_id(application_id: str) -> str:
        try:
            return str(uuid.UUID(application_id))
        except ValueError as e:
            raise InvalidParameterError("Invalid application_id format") from e

    @staticmethod
    def _validate_message(message: str) -> None:
        if not isinstance(message, str) or not message.strip():
            raise InvalidParameterError("Message must be non-empty")

    @staticmethod
    def _validate_additional_parameters(
        additional_parameters: Optional[Dict[str, Any]],
    ) -> None:
        if additional_parameters is not None and not isinstance(
            additional_parameters, dict
        ):
            raise InvalidParameterError("Additional parameters must be a dict or None")

    async def _send_request_async(
        self, endpoint: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        url = f"{self.hivetrace_url}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.hivetrace_access_token}"}
        try:
            response = await self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=httpx.Timeout(
                    connect=120.0, read=120.0, write=120.0, pool=120.0
                ),
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP error {e.response.status_code}",
                "details": e.response.text,
                "status_code": e.response.status_code,
            }
        except Exception as e:
            return {"error": str(e)}

    def _send_request_sync(
        self, endpoint: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        url = f"{self.hivetrace_url}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.hivetrace_access_token}"}
        try:
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=httpx.Timeout(
                    connect=120.0, read=120.0, write=120.0, pool=120.0
                ),
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP error {e.response.status_code}",
                "details": e.response.text,
                "status_code": e.response.status_code,
            }
        except Exception as e:
            return {"error": str(e)}

    async def input_async(
        self,
        application_id: str,
        message: str,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self._validate_application_id(application_id)
        self._validate_message(message)
        self._validate_additional_parameters(additional_parameters)

        payload = {
            "application_id": application_id,
            "message": message,
            "additional_parameters": additional_parameters or {},
        }
        return await self._send_request_async("/process_request/", payload)

    async def output_async(
        self,
        application_id: str,
        message: str,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self._validate_application_id(application_id)
        self._validate_message(message)
        self._validate_additional_parameters(additional_parameters)

        payload = {
            "application_id": application_id,
            "message": message,
            "additional_parameters": additional_parameters or {},
        }
        return await self._send_request_async("/process_response/", payload)

    async def function_call_async(
        self,
        application_id: str,
        tool_call_id: str,
        func_name: str,
        func_args: str,
        func_result: Optional[Union[Dict, str]] = None,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self._validate_application_id(application_id)
        self._validate_additional_parameters(additional_parameters)

        payload = {
            "application_id": application_id,
            "tool_call_id": tool_call_id,
            "func_name": func_name,
            "func_args": func_args,
            "func_result": func_result,
            "additional_parameters": additional_parameters or {},
        }
        return await self._send_request_async("/process_tool_call/", payload)

    def input(
        self,
        application_id: str,
        message: str,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self.async_mode:
            raise RuntimeError("Use input_async() in async mode")

        self._validate_application_id(application_id)
        self._validate_message(message)
        self._validate_additional_parameters(additional_parameters)

        payload = {
            "application_id": application_id,
            "message": message,
            "additional_parameters": additional_parameters or {},
        }
        return self._send_request_sync("/process_request/", payload)

    def output(
        self,
        application_id: str,
        message: str,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self.async_mode:
            raise RuntimeError("Use output_async() in async mode")

        self._validate_application_id(application_id)
        self._validate_message(message)
        self._validate_additional_parameters(additional_parameters)

        payload = {
            "application_id": application_id,
            "message": message,
            "additional_parameters": additional_parameters or {},
        }
        return self._send_request_sync("/process_response/", payload)

    def function_call(
        self,
        application_id: str,
        tool_call_id: str,
        func_name: str,
        func_args: str,
        func_result: Optional[Union[Dict, str]] = None,
        additional_parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self.async_mode:
            raise RuntimeError("Use function_call_async() in async mode")

        self._validate_application_id(application_id)
        self._validate_additional_parameters(additional_parameters)

        payload = {
            "application_id": application_id,
            "tool_call_id": tool_call_id,
            "func_name": func_name,
            "func_args": func_args,
            "func_result": func_result,
            "additional_parameters": additional_parameters or {},
        }
        return self._send_request_sync("/process_tool_call/", payload)

    async def close(self):
        if self.async_mode:
            await self.session.aclose()
        else:
            self.session.close()

    def __del__(self):
        if hasattr(self, "session"):
            if not self.async_mode:
                self.session.close()
            else:
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        loop.create_task(self.session.aclose())
                    else:
                        loop.run_until_complete(self.session.aclose())
                except:
                    pass
