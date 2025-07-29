"""
Monitored Crew implementation for CrewAI.
"""

from typing import Any, Dict, Optional

from crewai import Crew


class MonitoredCrew(Crew):
    """
    A monitored version of CrewAI's Crew class that logs all actions to HiveTrace.
    """

    model_config = {"extra": "allow"}

    def __init__(
        self,
        adapter,
        original_crew_agents,
        original_crew_tasks,
        original_crew_verbose,
        **kwargs,
    ):
        """
        Initialize the monitored crew.

        Parameters:
        - adapter: The CrewAI adapter instance
        - original_crew_agents: List of agents for the crew
        - original_crew_tasks: List of tasks for the crew
        - original_crew_verbose: Verbose flag from original crew
        - **kwargs: Additional parameters for the Crew class
        """
        super().__init__(
            agents=original_crew_agents,
            tasks=original_crew_tasks,
            verbose=original_crew_verbose,
            **kwargs,
        )
        self._adapter = adapter

    def _log_kickoff_result(
        self,
        result: Any,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_conversation_id: Optional[str] = None,
    ):
        """
        Log the final result of the crew execution.

        Parameters:
        - result: The result to log
        - user_id: ID of the user (runtime parameter)
        - session_id: ID of the session (runtime parameter)
        - agent_conversation_id: ID of the agents conversation (runtime parameter)
        """
        if result:
            result_str = str(result)

            final_message = f"[Final Result] {result_str}"
            agent_info_for_log = {}
            for agent in self.agents:
                if hasattr(agent, "agent_id") and hasattr(agent, "role"):
                    agent_info_for_log[agent.agent_id] = {
                        "name": agent.role,
                        "description": getattr(agent, "goal", ""),
                    }

            additional_params = {
                "agents": agent_info_for_log,
                "is_final_answer": True,
            }

            if user_id:
                additional_params["user_id"] = user_id
            if session_id:
                additional_params["session_id"] = session_id
            if agent_conversation_id:
                additional_params["agent_conversation_id"] = agent_conversation_id

            self._adapter._prepare_and_log(
                "output",
                self._adapter.async_mode,
                message_content=final_message,
                additional_params_from_caller=additional_params,
                force_log=True,
            )

    def kickoff(
        self,
        inputs: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_conversation_id: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        Start the crew's work and log the result.

        Parameters:
        - inputs: Inputs for the crew
        - user_id: ID of the user making the request (runtime parameter)
        - session_id: ID of the session (runtime parameter)
        - agent_conversation_id: ID of the agents conversation (runtime parameter)
        - *args, **kwargs: Additional arguments for the original kickoff

        Returns:
        - Result of the crew's work
        """
        self._adapter._reset_conversation_state()

        if user_id or session_id or agent_conversation_id:
            self._adapter._set_runtime_context(
                user_id=user_id,
                session_id=session_id,
                agent_conversation_id=agent_conversation_id,
            )

        if inputs is not None:
            result = super().kickoff(inputs=inputs, *args, **kwargs)
        else:
            result = super().kickoff(*args, **kwargs)

        self._log_kickoff_result(
            result,
            user_id=user_id,
            session_id=session_id,
            agent_conversation_id=agent_conversation_id,
        )
        return result

    async def kickoff_async(
        self,
        inputs: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_conversation_id: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        Start the crew's work asynchronously and log the result.

        Parameters:
        - inputs: Inputs for the crew
        - user_id: ID of the user making the request (runtime parameter)
        - session_id: ID of the session (runtime parameter)
        - agent_conversation_id: ID of the agents conversation (runtime parameter)
        - *args, **kwargs: Additional arguments for the original kickoff_async

        Returns:
        - Result of the crew's work
        """
        if not hasattr(super(), "kickoff_async"):
            raise NotImplementedError(
                "Async kickoff is not supported by the underlying crew's superclass"
            )

        self._adapter._reset_conversation_state()

        if user_id or session_id or agent_conversation_id:
            self._adapter._set_runtime_context(
                user_id=user_id,
                session_id=session_id,
                agent_conversation_id=agent_conversation_id,
            )

        if inputs is not None:
            result = await super().kickoff_async(inputs=inputs, *args, **kwargs)
        else:
            result = await super().kickoff_async(*args, **kwargs)

        self._log_kickoff_result(
            result,
            user_id=user_id,
            session_id=session_id,
            agent_conversation_id=agent_conversation_id,
        )
        return result
