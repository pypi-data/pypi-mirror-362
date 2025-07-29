from ..core.base import LLMBase
from ..core.messages import AIMessage, MessageBase
from ..core.config import LLMConfigBase
from typing import List, Union

try:
    from google import genai
except ImportError:
    raise ImportError("Package 'google' is not installed. Please install it using 'pip install light-ai[google]'.")





class GoogleLLMConfig(LLMConfigBase):
    """
    Configuration class for Google LLM models.
    
    Inherits from LLMConfigBase and adds specific parameters for Google LLMs.
    """
    pass


class GoogleLLM(LLMBase):
    def __init__(self, client: genai.Client, config: Union[GoogleLLMConfig, None] = None):
        super().__init__(config)
        self.client = client
        
        
    def _adapt_message_history(self, messages: List[MessageBase]) -> List[genai.types.Content]:
        """
        Convert a list of MessageBase objects to a list of strings.
        
        :param messages: List of MessageBase objects.
        :return: List of strings representing the contents of the messages.
        """
        contents = []
        for message in messages:
            if isinstance(message, AIMessage):
                contents.append(
                    genai.types.ModelContent(
                        parts=[genai.types.Part.from_text(text=message.content)],
                    )
                )
            else:
                contents.append(
                    genai.types.UserContent(
                        parts=[genai.types.Part.from_text(text='Why is the sky blue?')]
                    )
                )
        return contents
    
    def _adapt_config(self, config: GoogleLLMConfig) -> genai.types.GenerateContentConfig:
        """
        Convert GoogleLLMConfig to genai.types.GenerateContentConfig.
        
        :param config: An instance of GoogleLLMConfig.
        :return: An instance of genai.types.GenerateContentConfig.
        """
        return genai.types.GenerateContentConfig(
            system_instruction=config.system_prompt,
            max_output_tokens=config.max_output_tokens,
            max_input_tokens=config.max_input_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
        )

    def invoke(self, messages: List[MessageBase])-> AIMessage:
        """
        Generate text using the Gemini model.
        """
        ai_response = AIMessage(
            content=self.client.models.generate_content(
                model=self.config.model_name,
                contents=self._adapt_message_history(messages),
                config=self._adapt_config(self.config) if self.config else genai.types.GenerateContentConfig()
            )
        )
        return ai_response