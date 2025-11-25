import os
import logging
from typing import Dict, Any
import anthropic
from .base_ai_client import BaseAIClient

logger = logging.getLogger(__name__)

class AnthropicClient(BaseAIClient):
    """Anthropic Claude API client implementation"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key or os.getenv('ANTHROPIC_API_KEY'))
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-sonnet-20240229"
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion using Anthropic Claude API"""
        if not self.validate_api_key():
            return "Error: Anthropic API key not configured"
        
        try:
            response = self.client.messages.create(
                model=kwargs.get('model', self.model),
                max_tokens=kwargs.get('max_tokens', 4000),
                temperature=kwargs.get('temperature', 0.7),
                system="You are an expert full-stack web developer.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            self.total_tokens_used += response.usage.input_tokens + response.usage.output_tokens
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            return f"Error generating completion: {str(e)}"
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            'total_tokens_used': self.total_tokens_used,
            'model': self.model
        }