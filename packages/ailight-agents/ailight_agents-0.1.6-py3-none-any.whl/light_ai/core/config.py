import os
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class LLMConfigBase:
    """
    Base class for LLM model configuration.
    Contains common parameters and logic for handling API keys.
    """
    # Models parameters
    model_name:str = ""
    temperature: float = 0.7
    top_p: float = 1.0
    system_prompt: Optional[str] = ""
    max_output_tokens: Optional[int] = None
    
    # Invocation retry logic parameters
    retry_enabled: bool = False
    trigger_retry_keywords: List[str] = field(default_factory=lambda:[''])
    max_retries: int = 3
    base_delay: float = 1.0 # seconds
    max_delay: float = 60.0 # seconds
    backoff_multiplier: float = 2.0 # exponential backoff multiplier
    retry_jitter_enabled: bool = True
    
    