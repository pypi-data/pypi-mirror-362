"""
Decorator implementation for CrewAI tracking.
"""

import functools
from typing import Callable, Dict, Optional

from hivetrace.adapters.crewai.adapter import CrewAIAdapter


def trace(
    hivetrace,
    application_id: Optional[str] = None,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    agent_id_mapping: Optional[Dict[str, Dict[str, str]]] = None,
):
    """
    Decorator for tracking the CrewAI crew.
    Creates an adapter and applies it to the crew setup function.

    Parameters:
    - hivetrace: The hivetrace instance for logging
    - application_id: ID of the application in Hivetrace
    - user_id: ID of the user in Hivetrace
    - session_id: ID of the session in Hivetrace
    - agent_id_mapping: Mapping from agent role names to their metadata dict with 'id' and 'description'
                         e.g. {"Content Planner": {"id": "planner-123", "description": "Creates content plans"}}

    Returns:
    - Decorator function to wrap a crew setup function
    """
    if callable(hivetrace):
        raise ValueError(
            "trace requires at least the hivetrace parameter. "
            "Use @trace (hivetrace=your_hivetrace_instance)"
        )

    adapter = CrewAIAdapter(
        hivetrace=hivetrace,
        application_id=application_id,
        user_id=user_id,
        session_id=session_id,
        agent_id_mapping=agent_id_mapping if agent_id_mapping is not None else {},
    )

    def decorator(crew_setup_func: Callable):
        """
        Decorator for crew setup functions.

        Parameters:
        - crew_setup_func: Function that sets up and returns a CrewAI crew

        Returns:
        - Wrapped function that returns a monitored crew
        """

        @functools.wraps(crew_setup_func)
        def wrapper(*args, **kwargs):
            crew = crew_setup_func(*args, **kwargs)
            return adapter.wrap_crew(crew)

        return wrapper

    return decorator
