from .hivetrace import (
    HivetraceSDK,
    InvalidParameterError,
    MissingConfigError,
    UnauthorizedError,
)

__all__ = [
    "HivetraceSDK",
    "InvalidParameterError",
    "MissingConfigError",
    "UnauthorizedError",
]

try:
    from hivetrace.crewai_adapter import CrewAIAdapter as _CrewAIAdapter
    from hivetrace.crewai_adapter import trace as _crewai_trace

    CrewAIAdapter = _CrewAIAdapter
    crewai_trace = _crewai_trace
    trace = _crewai_trace

    __all__.extend(["CrewAIAdapter", "crewai_trace", "trace"])
except ImportError:
    pass

try:
    from hivetrace.adapters.langchain import LangChainAdapter as _LangChainAdapter
    from hivetrace.adapters.langchain import trace as _langchain_trace

    LangChainAdapter = _LangChainAdapter
    langchain_trace = _langchain_trace

    __all__.extend(["LangChainAdapter", "langchain_trace"])
except ImportError:
    pass
