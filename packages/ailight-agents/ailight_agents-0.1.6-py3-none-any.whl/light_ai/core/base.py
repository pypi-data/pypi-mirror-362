import time
import random
from typing import List, Union
from abc import ABC, abstractmethod
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
        
    def _should_retry(self, exception) -> bool:
        """
        Check if the exception contains any trigger keywords that indicate a retry is needed.
        
        :param exception: The exception or response to check.
        :return: True if retry is needed, False otherwise.
        """
        if not self.config.retry_enabled:
            return False
        
        message = ""
        
        if hasattr(exception, 'message'):
            message = exception.message.lower()
        else:
            message = str(exception).lower()
            
        if hasattr(exception, 'status_code'):
            message += f" status_code: {exception.status_code}"
        
        message = message.lower()
        return any(keyword in message for keyword in self.config.trigger_retry_keywords)
    
    def _calculate_delay(self, attempt_number: int) -> float:
        """
        Calculate the delay before the next retry attempt.
        
        :param attempt_number: The current attempt number (0-based).
        :return: The calculated delay in seconds.
        """
        delay = self.config.base_delay * (self.config.backoff_multiplier ** attempt_number)
        delay = min(delay, self.config.max_delay)
        if self.config.retry_jitter_enabled:
            jitter = random.uniform(0, delay)
            delay += jitter
        return delay
    
    @abstractmethod
    def _call_model(self, messages: List[MessageBase]) -> AIMessage:
        """
        Calls the model with the provided messages and returns the AI response.
        
        :param messages: List of MessageBase objects representing the conversation history.
        :return: An instance of AIMessage containing the model's response.
        """
        pass
        
    def invoke(self, messages: List[MessageBase])-> AIMessage:
        """
        Invoke the model with a list of messages and waits for an answer.
        """
        last_attempt = 0
        for attempt in range(self.config.max_retries):
            try:
                return self._call_model(messages)
            except Exception as e:
                if not self.config.retry_enabled or attempt == self.config.max_retries:
                    raise Exception(f"Failed to generate content after {self.config.max_retries} attempts: {e}")

                if not self._should_retry(e):
                    raise Exception(f"Retry not triggered for exception: {e}")
                
                delay = self._calculate_delay(attempt)
                time.sleep(delay)
                last_attempt += 1
        raise Exception(f"Max retries (done: {last_attempt}) reached without a successful response.")
    
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
