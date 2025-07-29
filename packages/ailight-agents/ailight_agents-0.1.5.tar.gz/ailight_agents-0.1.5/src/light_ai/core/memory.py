from .base import MemoryBase
from .messages import MessageBase
from time import time
from typing import List, Dict, Tuple, Union

class ChatMemory(MemoryBase):
    """
    Class for user memory management.
    """
    __slots__ = 'user_id', 'memory', 'last_access'
    user_id: Union[str, None]
    memory: List[MessageBase]
    last_access: float
    
    def __init__(self, user_id: Union[str, None] = None):
        """
        Initializes the MemoryBase with a user ID.
        
        :param user_id: The unique identifier for the user.
        """
        self.user_id = user_id
        self.memory = []
        self.last_access = time()
        
    def add_message(self, message: MessageBase):
        """
        Add a message to the memory and update the last access time.
        
        :param message: The message to be added, which should be an instance of MessageBase.
        """
        self.memory.append(message)
        self.last_access = time()
        
    def get_history(self):
        """
        Get all messages in the memory.
        
        :return: A list of messages stored in the memory.
        """
        return self.memory


class MultiChatMemory:
    """
    Manages conversation histories for multiple users.
    Each user has their own memory instance, allowing for independent conversation histories.
    Each access to a user's memory updates the last access time.
    """
    
    __slots__ = '_pool'
    _pool: Dict[str, MemoryBase]

    def __init__(self): 
        self._pool = {}
            
            
    def _new_user_memory(self, user_id: str) -> MemoryBase:
        """
        Create a new memory for a user.
        
        :param user_id: The unique identifier for the user.
        :return: A new MemoryBase instance for the user.
        """
        return self._pool.setdefault(user_id, MemoryBase(user_id))
        
    def get_conversation_history(self, user_id: str) -> Tuple[MemoryBase, bool]:
        """
        Get the memory for a user, creating it if it doesn't exist.
        
        :param user_id: The unique identifier for the user.
        :return: A tuple containing the user's memory and a boolean indicating if it was newly created.
        """
        # create new memory if does not exist
        if user_id not in self._pool:
            return self._new_user_memory(user_id), True
        # otherwise update last access time
        self._pool[user_id].last_access = time()
        return self._pool[user_id], False
    
    def get_conversation_history_json(self, user_id: str) -> List[Dict]:
        """
        Get the conversation history for a user as a dictionary.
        If the memory does not exist, it creates a new one.
        
        :param user_id: The unique identifier for the user.
        
        :return: A list of dictionaries representing the conversation history.
        """
        memory, _ = self.get_conversation_history(user_id)
        return [msg.to_dict() for msg in memory.get_messages()]
    
    def add_message(self, user_id: str, message: MessageBase):
        """
        Add a user message to the user's memory. 
        If no message for the user exists, it creates a new memory for the user.
        
        :param user_id: The unique identifier for the user.
        :param message: The message to be added, which can be a UserMessage or AIMessage.
        :return: None
        """
        memory = None
        if user_id not in self._pool:
            memory = self._new_user_memory(user_id)
        else:
            memory = self._pool[user_id]
        memory.add_message(message)