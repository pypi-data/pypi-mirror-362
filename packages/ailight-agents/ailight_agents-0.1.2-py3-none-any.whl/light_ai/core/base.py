from abc import ABC, abstractmethod
from typing import List, Union
from .messages import MessageBase, AIMessage
from .config import LLMConfigBase



class LLMBase(ABC):   
    __slots__ = 'client', 'config'
    
    def __init__(self, config: Union[LLMConfigBase, None] = None):
        """
        Initialize the LLMBase with a configuration object.
        
        :param config: An instance of LLMConfigBase or None.
        """
        self.config = config if config else LLMConfigBase()
        
    @abstractmethod
    def invoke(self, messages: List[MessageBase])-> AIMessage:
        """
        Invoke the model with a list of messages and waits for an answer.
        """
        pass
    
    
class MemoryBase:
    """
    Base class for user memory management.
    This class is intended to be extended by specific user memory implementations.
    """
    @abstractmethod
    def add_message(seld, message: MessageBase) -> None:
        """Adds a message to the history
        
        :param message: The message to be added, which should be an instance of MessageBase.
        """
        pass
    
    @abstractmethod
    def get_history(self) -> List[MessageBase]:
        """Returns the history of messages
        
        :return: A list of messages stored in the memory.
        """
        pass
