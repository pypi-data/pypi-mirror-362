from .core.base import LLMBase, MemoryBase
from .core.messages import UserMessage, AIMessage

class Agent:
    def __init__(self, llm: LLMBase, memory: MemoryBase):
        self.llm = llm
        self.memory = memory

    def run(self, user_input: str) -> str:
        # 1. Add the user input to memory
        user_message = UserMessage(content=user_input)
        self.memory.add_message(user_message)

        # 2. Take complete chat history from memory
        chat_history = self.memory.get_history()

        # 3. Invoke the LLM with the chat history
        ai_response = self.llm.invoke(chat_history)

        # 4. Add the AI response to memory
        self.memory.add_message(ai_response)

        return ai_response.content