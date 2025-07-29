"""
Light AI - A lightweight AI agent framework
"""

__version__ = "0.1.0"

# Core exports
from .core.base import LLMBase, MemoryBase
from .core.messages import MessageBase, UserMessage, AIMessage
from .core.config import LLMConfigBase
from .core.memory import ChatMemory, MultiChatMemory
from .agent import Agent
from .graphs.graph import Graph, GraphState
from .graphs.graph_agent import GraphAgentBase

__all__ = [
    "LLMBase",
    "MemoryBase", 
    "MessageBase",
    "UserMessage",
    "AIMessage",
    "LLMConfigBase",
    "ChatMemory",
    "MultiChatMemory",
    "Agent",
    "Graph",
    "GraphState",
    "GraphAgentBase",
]

# Optional imports with graceful fallback
try:
    from .llms.google import GoogleLLM, GoogleLLMConfig
    __all__.extend(["GoogleLLM", "GoogleLLMConfig"])
except ImportError:
    pass