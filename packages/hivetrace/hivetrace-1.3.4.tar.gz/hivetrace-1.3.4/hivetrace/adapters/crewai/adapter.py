"""
The main implementation of the CrewAI adapter.
"""

import asyncio
from typing import Any, Dict, Optional

from crewai import Agent, Crew, Task

from hivetrace.adapters.base_adapter import BaseAdapter
from hivetrace.adapters.crewai.monitored_agent import MonitoredAgent
from hivetrace.adapters.crewai.monitored_crew import MonitoredCrew
from hivetrace.adapters.crewai.tool_wrapper import wrap_tool
from hivetrace.adapters.utils.logging import process_agent_params
from hivetrace.utils.uuid_generator import generate_uuid


class CrewAIAdapter(BaseAdapter):
    """
    Adapter for monitoring CrewAI agents with Hivetrace.
    """

    def __init__(
        self,
        hivetrace,
        application_id: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_id_mapping: Optional[Dict[str, Dict[str, str]]] = None,
    ):
        """
        Initialize the CrewAI adapter.

        Parameters:
        - hivetrace: Instance of hivetrace for logging
        - application_id: ID of the application in Hivetrace
        - user_id: ID of the user in the conversation (can be overridden at runtime)
        - session_id: ID of the session in the conversation (can be overridden at runtime)
        - agent_id_mapping: Mapping of agent roles to their IDs
        """
        super().__init__(hivetrace, application_id, user_id, session_id)
        self.agent_id_mapping = agent_id_mapping if agent_id_mapping is not None else {}
        self.agents_info = {}
        self._runtime_user_id = None
        self._runtime_session_id = None
        self._runtime_agents_conversation_id = None
        self._current_parent_agent_id = None
        self._conversation_started = False
        self._first_agent_logged = False
        self._recent_messages = []
        self._max_recent_messages = 5

    def _reset_conversation_state(self):
        """
        Reset the conversation state for a new command execution.
        """
        self._conversation_started = False
        self._first_agent_logged = False
        self._current_parent_agent_id = None

    def _set_current_parent(self, agent_id: str):
        """
        Set the current agent as the parent for subsequent operations.
        """
        self._current_parent_agent_id = agent_id

    def _clear_current_parent(self):
        """
        Clear the current parent when the agent finishes its work.
        """
        self._current_parent_agent_id = None

    def _get_current_parent_id(self) -> Optional[str]:
        """
        Get the ID of the current parent agent.
        """
        return self._current_parent_agent_id

    def _set_runtime_context(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_conversation_id: Optional[str] = None,
    ):
        """
        Set the execution context for user_id, session_id and agent_conversation_id.

        Parameters:
        - user_id: Runtime user ID (overrides the constructor value)
        - session_id: Runtime session ID (overrides the constructor value)
        - agent_conversation_id: Runtime agents conversation ID
        """
        self._runtime_user_id = user_id
        self._runtime_session_id = session_id
        self._runtime_agents_conversation_id = agent_conversation_id

    def _get_effective_user_id(self) -> Optional[str]:
        """Get the user_id."""
        return self._runtime_user_id or self.user_id

    def _get_effective_session_id(self) -> Optional[str]:
        """Get the session_id."""
        return self._runtime_session_id or self.session_id

    def _get_effective_agents_conversation_id(self) -> Optional[str]:
        """Get the agent_conversation_id."""
        return self._runtime_agents_conversation_id

    def _should_skip_deduplication(
        self, message_content: Optional[str], force_log: bool
    ) -> bool:
        """
        Determine if deduplication should be skipped for the message.
        """
        return (
            force_log
            or (message_content and message_content.startswith("["))
            or (message_content and "Thought" in message_content)
            or (message_content and "working on" in message_content)
        )

    def _handle_deduplication(self, message_content: str) -> bool:
        """
        Handle message deduplication.
        """
        message_hash = hash(message_content)
        if message_hash in self._recent_messages:
            return True

        self._recent_messages.append(message_hash)
        if len(self._recent_messages) > self._max_recent_messages:
            self._recent_messages.pop(0)

        return False

    def _prepare_effective_params(
        self, additional_params_from_caller: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Prepare parameters considering runtime values.
        """
        final_params = additional_params_from_caller or {}

        effective_user_id = self._get_effective_user_id()
        effective_session_id = self._get_effective_session_id()
        effective_agents_conversation_id = self._get_effective_agents_conversation_id()

        if effective_user_id:
            final_params.setdefault("user_id", effective_user_id)
        if effective_session_id:
            final_params.setdefault("session_id", effective_session_id)
        if effective_agents_conversation_id:
            final_params.setdefault(
                "agent_conversation_id", effective_agents_conversation_id
            )

        final_params.setdefault("is_final_answer", False)

        return final_params

    def _handle_agent_parent_id(self, final_params: Dict[str, Any]) -> None:
        """
        Handle adding parent_id to agents.
        """
        if not ("agents" in final_params and isinstance(final_params["agents"], dict)):
            return

        agent_parent_id = self._get_current_parent_id()

        if not self._first_agent_logged and not self._conversation_started:
            self._first_agent_logged = True
            self._conversation_started = True
        elif agent_parent_id:
            for agent_id, agent_info in final_params["agents"].items():
                if isinstance(agent_info, dict):
                    agent_info["agent_parent_id"] = agent_parent_id

    def _build_log_kwargs(
        self,
        log_method_name_stem: str,
        message_content: Optional[str],
        tool_call_details: Optional[Dict[str, Any]],
        final_params: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Create arguments for the logging method call.
        """
        log_kwargs = {
            "application_id": self.application_id,
            "additional_parameters": final_params,
        }

        if log_method_name_stem in ["input", "output"]:
            if message_content is None:
                return None
            log_kwargs["message"] = message_content
        elif log_method_name_stem == "function_call":
            if tool_call_details is None:
                return None
            log_kwargs.update(tool_call_details)
        else:
            return None

        return log_kwargs

    def _execute_log(
        self, log_method_name_stem: str, is_async: bool, log_kwargs: Dict[str, Any]
    ) -> None:
        """
        Execute logging with error handling.
        """
        method_to_call_name = f"{log_method_name_stem}{'_async' if is_async else ''}"

        try:
            actual_log_method = getattr(self.trace, method_to_call_name)
            if is_async:
                asyncio.create_task(actual_log_method(**log_kwargs))
            else:
                actual_log_method(**log_kwargs)
        except AttributeError:
            print(f"Error: Hivetrace object does not have method {method_to_call_name}")
        except Exception as e:
            print(f"Error logging {log_method_name_stem} to Hivetrace: {e}")

    def _prepare_and_log(
        self,
        log_method_name_stem: str,
        is_async: bool,
        message_content: Optional[str] = None,
        tool_call_details: Optional[Dict[str, Any]] = None,
        additional_params_from_caller: Optional[Dict[str, Any]] = None,
        force_log: bool = False,
    ) -> None:
        """
        Override the base method to use user_id, session_id and agent_conversation_id.
        """
        should_skip_deduplication = self._should_skip_deduplication(
            message_content, force_log
        )

        if not should_skip_deduplication and message_content:
            if self._handle_deduplication(message_content):
                return

        final_params = self._prepare_effective_params(additional_params_from_caller)

        self._handle_agent_parent_id(final_params)

        log_kwargs = self._build_log_kwargs(
            log_method_name_stem, message_content, tool_call_details, final_params
        )
        if log_kwargs is None:
            return

        self._execute_log(log_method_name_stem, is_async, log_kwargs)

    def _get_agent_mapping(self, role: str) -> Dict[str, str]:
        """
        Get the agent ID and description from the mapping.
        """
        if self.agent_id_mapping and role in self.agent_id_mapping:
            mapping_data = self.agent_id_mapping[role]
            if isinstance(mapping_data, dict):
                return {
                    "id": mapping_data.get("id", generate_uuid()),
                    "description": mapping_data.get("description", ""),
                }
            elif isinstance(mapping_data, str):
                return {"id": mapping_data, "description": ""}

        return {"id": generate_uuid(), "description": ""}

    async def output_async(
        self,
        message: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Asynchronous logging of agent output to Hivetrace.
        """
        if not self.async_mode:
            raise RuntimeError("Cannot use async methods when SDK is in sync mode")

        processed_params = process_agent_params(additional_params)

        self._prepare_and_log(
            "output",
            True,
            message_content=message,
            additional_params_from_caller=processed_params,
            force_log=False,
        )

    def output(
        self,
        message: str,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Synchronous logging of agent output to Hivetrace.
        """
        if self.async_mode:
            raise RuntimeError("Cannot use sync methods when SDK is in async mode")

        processed_params = process_agent_params(additional_params)

        self._prepare_and_log(
            "output",
            False,
            message_content=message,
            additional_params_from_caller=processed_params,
            force_log=False,
        )

    def agent_callback(self, message: Any) -> None:
        """
        Callback for agent actions.
        """
        message_text: str
        additional_params_for_log: Dict[str, Any]

        if isinstance(message, dict) and message.get("type") == "agent_thought":
            agent_id_from_message = message.get("agent_id")
            role = message.get("role", "")

            agent_mapping = self._get_agent_mapping(role)
            final_agent_id = agent_id_from_message or agent_mapping.get("id")

            agent_info_details = {
                "name": message.get("agent_name", role),
                "description": agent_mapping.get(
                    "description", message.get("agent_description", "Agent thought")
                ),
            }
            message_text = f"Thought from agent {role}: {message['thought']}"
            additional_params_for_log = {"agents": {final_agent_id: agent_info_details}}

            self._set_current_parent(final_agent_id)
        else:
            message_text = str(message)
            additional_params_for_log = {"agents": self.agents_info}

        self._prepare_and_log(
            "input",
            self.async_mode,
            message_content=message_text,
            additional_params_from_caller=additional_params_for_log,
            force_log=True,
        )

    def task_callback(self, message: Any) -> None:
        """
        Handler for task messages.
        Formats and logs task messages to Hivetrace.
        """
        message_text = ""
        agent_info_for_log = {}

        if hasattr(message, "__dict__"):
            current_agent_role = ""
            current_agent_id = None

            if hasattr(message, "agent"):
                agent_value = message.agent
                if isinstance(agent_value, str):
                    current_agent_role = agent_value
                elif hasattr(agent_value, "role"):
                    current_agent_role = agent_value.role

                if current_agent_role:
                    agent_mapping = self._get_agent_mapping(current_agent_role)
                    current_agent_id = agent_mapping["id"]

                    agent_info_for_log = {
                        current_agent_id: {
                            "name": current_agent_role,
                            "description": agent_mapping["description"]
                            or (
                                getattr(agent_value, "goal", "")
                                if hasattr(agent_value, "goal")
                                else "Task agent"
                            ),
                        }
                    }

            message_content = ""

            if hasattr(message, "raw") and message.raw:
                message_content = str(message.raw)
            else:
                message_parts = []

                for field_name in [
                    "status",
                    "step",
                    "action",
                    "observation",
                    "thought",
                ]:
                    if hasattr(message, field_name):
                        field_value = getattr(message, field_name)
                        if field_value:
                            message_parts.append(f"{field_name}: {str(field_value)}")

                if not message_parts:
                    message_parts.append(str(message))

                message_content = "; ".join(message_parts)

            if message_content:
                self._prepare_and_log(
                    "output",
                    self.async_mode,
                    message_content=message_content,
                    additional_params_from_caller={"agents": agent_info_for_log},
                    force_log=True,
                )

            if current_agent_id:
                self._set_current_parent(current_agent_id)
        else:
            message_text = f"[Task] {str(message)}"
            self._prepare_and_log(
                "output",
                self.async_mode,
                message_content=message_text,
                additional_params_from_caller={"agents": agent_info_for_log},
                force_log=True,
            )

    def _wrap_agent(self, agent: Agent) -> Agent:
        """
        Wraps an agent for monitoring its actions.
        """
        agent_mapping = self._get_agent_mapping(agent.role)
        agent_id_for_monitored_agent = agent_mapping["id"]

        agent_props = agent.__dict__.copy()

        original_tools = getattr(agent, "tools", [])
        wrapped_tools = [wrap_tool(tool, agent.role, self) for tool in original_tools]
        agent_props["tools"] = wrapped_tools

        for key_to_remove in ["id", "agent_executor", "agent_ops_agent_id"]:
            if key_to_remove in agent_props:
                del agent_props[key_to_remove]

        monitored_agent = MonitoredAgent(
            adapter_instance=self,
            callback_func=self.agent_callback,
            agent_id=agent_id_for_monitored_agent,
            **agent_props,
        )

        return monitored_agent

    def _wrap_task(self, task: Task) -> Task:
        """
        Wraps a task for monitoring its actions.
        """
        original_callback = task.callback

        def combined_callback(message):
            self.task_callback(message)
            if original_callback:
                original_callback(message)

        task.callback = combined_callback
        return task

    def wrap_crew(self, crew: Crew) -> Crew:
        """
        Adds monitoring to an existing CrewAI crew.
        Wraps all agents and tasks in the crew, as well as the kickoff methods.
        """
        self._reset_conversation_state()

        current_agents_info = {}

        for agent_instance in crew.agents:
            if hasattr(agent_instance, "role"):
                agent_mapping = self._get_agent_mapping(agent_instance.role)
                agent_id = agent_mapping["id"]
                description = agent_mapping["description"] or getattr(
                    agent_instance, "goal", ""
                )
                current_agents_info[agent_id] = {
                    "name": agent_instance.role,
                    "description": description,
                }

        self.agents_info = current_agents_info

        wrapped_agents = [self._wrap_agent(agent) for agent in crew.agents]
        wrapped_tasks = [self._wrap_task(task) for task in crew.tasks]

        monitored_crew_instance = MonitoredCrew(
            original_crew_agents=wrapped_agents,
            original_crew_tasks=wrapped_tasks,
            original_crew_verbose=crew.verbose,
            manager_llm=getattr(crew, "manager_llm", None),
            memory=getattr(crew, "memory", None),
            process=getattr(crew, "process", None),
            config=getattr(crew, "config", None),
            adapter=self,
        )
        return monitored_crew_instance
