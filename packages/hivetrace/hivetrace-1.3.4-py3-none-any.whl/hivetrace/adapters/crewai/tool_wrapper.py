"""
Tool wrapping utilities for CrewAI adapter.
"""

import functools
from typing import Any, Callable

from hivetrace.utils.uuid_generator import generate_uuid


def wrap_tool_function(
    func: Callable,
    func_name: str,
    agent_role: str,
    adapter_instance,
) -> Callable:
    """
    Wraps a tool function to monitor its calls, attributing to the specified agent_role.

    Parameters:
    - func: The function to wrap
    - func_name: Name of the function
    - agent_role: Role of the agent using this tool
    - adapter_instance: The CrewAI adapter instance

    Returns:
    - Wrapped function that logs calls to HiveTrace
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_list_str = [str(arg) for arg in args]
        kwargs_list_str = [f"{k}={v}" for k, v in kwargs.items()]
        all_args_str = ", ".join(args_list_str + kwargs_list_str)

        result = func(*args, **kwargs)

        agent_mapping = adapter_instance._get_agent_mapping(agent_role)
        mapped_agent_id = agent_mapping["id"]
        mapped_agent_description = agent_mapping["description"]

        tool_call_id = generate_uuid()

        tool_call_details = {
            "tool_call_id": tool_call_id,
            "func_name": func_name,
            "func_args": all_args_str,
            "func_result": str(result),
        }

        additional_params_for_log = {
            "agents": {
                mapped_agent_id: {
                    "name": agent_role,
                    "description": mapped_agent_description,
                }
            },
        }

        adapter_instance._prepare_and_log(
            "function_call",
            adapter_instance.async_mode,
            tool_call_details=tool_call_details,
            additional_params_from_caller=additional_params_for_log,
            force_log=False,
        )
        return result

    return wrapper


def wrap_tool(tool: Any, agent_role: str, adapter_instance) -> Any:
    """
    Wraps a tool's _run method to monitor its calls, passing the agent_role.

    Parameters:
    - tool: The tool object to wrap
    - agent_role: Role of the agent using this tool
    - adapter_instance: The CrewAI adapter instance

    Returns:
    - Tool with wrapped _run method
    """
    if hasattr(tool, "_run") and callable(tool._run):
        if getattr(tool._run, "_is_hivetrace_wrapped", False):
            return tool
        wrapped = wrap_tool_function(
            tool._run,
            tool.name if hasattr(tool, "name") else "unknown_tool",
            agent_role,
            adapter_instance,
        )
        wrapped._is_hivetrace_wrapped = True
        tool._run = wrapped
    return tool
