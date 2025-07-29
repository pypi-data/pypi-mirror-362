import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class LLMConfigBase:
    """
    Base class for LLM model configuration.
    Contains common parameters and logic for handling API keys.
    """
    model_name:str = ""
    temperature: float = 0.7
    top_p: float = 1.0
    system_prompt: Optional[str] = ""
    max_input_tokens: Optional[int] = None
    max_output_tokens: Optional[int] = None