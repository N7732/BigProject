from abc import ABC, abstractmethod
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BaseAIClient(ABC):
    """Abstract base class for AI clients"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.total_tokens_used = 0
    
    @abstractmethod
    def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion for given prompt"""
        pass
    
    @abstractmethod
    def get_usage_stats(self) -> dict[str, Any]:
        """Get usage statistics"""
        pass
    
    def validate_api_key(self) -> bool:
        """Validate API key is present"""
        if not self.api_key:
            logger.error("API key not configured")
            return False
        return True