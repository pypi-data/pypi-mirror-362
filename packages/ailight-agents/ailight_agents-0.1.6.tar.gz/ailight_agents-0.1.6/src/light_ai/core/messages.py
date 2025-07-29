from dataclasses import dataclass
from typing import Literal 

@dataclass(frozen=True)
class MessageBase:
    """
    Base class for messages in the Light AI system.
    This class is intended to be extended by specific message types.
    """
    __slots__ = 'content', 'role'
    content: str
    role: Literal['system', 'user', 'ai', 'model', 'tool']

    def __str__(self):
        """
        Returns a string representation of the message.

        :return: The content of the message.
        """
        return f"{self.role}: {self.content}"
    
    def to_dict(self):
        """
        Converts the message to a dictionary representation.

        :return: A dictionary containing the message content.
        """
        return {
            "content": self.content,
            "role": getattr(self, "role", "unknown")  # Default role if not set
        }
        
@dataclass(frozen=True) 
class UserMessage(MessageBase):
    """
    Represents a message from a user.
    Inherits from MessageBase.
    
    It has the following attributes:
    - content: The content of the user message.
    - role: The role of the message, which is set to "user" for user
    """
    role: Literal['user'] = 'user'
    
@dataclass(frozen=True)    
class AIMessage(MessageBase):
    """
    Represents a message from an AI.
    Inherits from MessageBase.
    
    It has the following attributes:
    - content: The content of the AI message.
    - role: The role of the message, which is set to "model" for AI
    """
    role: Literal['ai', 'model'] = 'model'
    