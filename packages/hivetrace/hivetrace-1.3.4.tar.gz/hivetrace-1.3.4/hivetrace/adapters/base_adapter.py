"""
Base adapter class for HiveTrace integrations.
"""

from typing import Any, Dict, Optional


class BaseAdapter:
    """
    Base class for all integration adapters for Hivetrace.

    This class defines the common interface and utilities used by all adapters.
    Specific adapters should inherit from this class and implement the required methods.
    """

    def __init__(
        self,
        hivetrace,
        application_id: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        """
        Initialize the base adapter.

        Parameters:
        - hivetrace: The hivetrace instance for logging
        - application_id: ID of the application in Hivetrace
        - user_id: ID of the user in the conversation
        - session_id: ID of the session in the conversation
        """
        self.trace = hivetrace
        self.application_id = application_id
        self.user_id = user_id
        self.session_id = session_id
        self.async_mode = self.trace.async_mode

    def _prepare_and_log(
        self,
        log_method_name_stem: str,
        is_async: bool,
        message_content: Optional[str] = None,
        tool_call_details: Optional[Dict[str, Any]] = None,
        additional_params_from_caller: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Helper method to prepare parameters and log to Hivetrace.

        Parameters:
        - log_method_name_stem: Base name of the logging method ('input', 'output', 'function_call')
        - is_async: Whether to use async logging methods
        - message_content: Content of the message to log (for input/output)
        - tool_call_details: Details of tool/function call (for function_call)
        - additional_params_from_caller: Additional parameters to include in the log
        """
        final_additional_params = additional_params_from_caller or {}
        final_additional_params.setdefault("user_id", self.user_id)
        final_additional_params.setdefault("session_id", self.session_id)

        log_kwargs = {
            "application_id": self.application_id,
            "additional_parameters": final_additional_params,
        }

        if log_method_name_stem in ["input", "output"]:
            if message_content is None:
                print(f"Warning: message_content is None for {log_method_name_stem}")
                return
            log_kwargs["message"] = message_content
        elif log_method_name_stem == "function_call":
            if tool_call_details is None:
                print("Warning: tool_call_details is None for function_call")
                return
            log_kwargs.update(tool_call_details)
        else:
            print(f"Error: Unsupported log_method_name_stem: {log_method_name_stem}")
            return

        method_to_call_name = f"{log_method_name_stem}{'_async' if is_async else ''}"

        try:
            actual_log_method = getattr(self.trace, method_to_call_name)
            if is_async:
                import asyncio

                asyncio.create_task(actual_log_method(**log_kwargs))
            else:
                actual_log_method(**log_kwargs)
        except AttributeError:
            print(f"Error: Hivetrace object does not have method {method_to_call_name}")
        except Exception as e:
            print(f"Error logging {log_method_name_stem} to Hivetrace: {e}")

    async def input_async(
        self, message: str, additional_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Asynchronously logs user input to Hivetrace.
        """
        if not self.async_mode:
            raise RuntimeError("Cannot use async methods when SDK is in sync mode")

        self._prepare_and_log(
            "input",
            True,
            message_content=message,
            additional_params_from_caller=additional_params,
        )

    def input(
        self, message: str, additional_params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Synchronously logs user input to Hivetrace.
        """
        if self.async_mode:
            raise RuntimeError("Cannot use sync methods when SDK is in async mode")

        self._prepare_and_log(
            "input",
            False,
            message_content=message,
            additional_params_from_caller=additional_params,
        )

    async def output_async(
        self,
        message: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Asynchronously logs agent output to Hivetrace.
        """
        if not self.async_mode:
            raise RuntimeError("Cannot use async methods when SDK is in sync mode")

        self._prepare_and_log(
            "output",
            True,
            message_content=message,
            additional_params_from_caller=additional_params,
        )

    def output(
        self,
        message: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Synchronously logs agent output to Hivetrace.
        """
        if self.async_mode:
            raise RuntimeError("Cannot use sync methods when SDK is in async mode")

        self._prepare_and_log(
            "output",
            False,
            message_content=message,
            additional_params_from_caller=additional_params,
        )
