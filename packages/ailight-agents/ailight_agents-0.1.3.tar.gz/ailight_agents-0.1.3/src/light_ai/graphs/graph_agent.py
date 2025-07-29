from ..core.base import LLMBase
from abc import ABC, abstractmethod

class GraphAgentBase(ABC):
    """GraphAgent is a specialized agent that can be used in a graph context.
    """
    __slots__ = ('llm',)
    
    def __init__(self, llm: LLMBase):
        self.llm = llm
    
    @abstractmethod
    def __call__(self, state: str) -> dict:
        """
        Executes the agent with the given state and returns a dictionary of actions.
        """
        raise NotImplementedError("__call__ method not implemented in GraphAgentBase")
    