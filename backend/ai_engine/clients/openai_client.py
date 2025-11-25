import os
import logging
from typing import Dict, Any
from openai import OpenAI
from .base_ai_client import BaseAIClient

logger = logging.getLogger(__name__)

class OpenAIClient(BaseAIClient):
    """OpenAI API client implementation"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key or os.getenv('OPENAI_API_KEY'))
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4"  # or "gpt-3.5-turbo" for cost savings
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion using OpenAI API"""
        if not self.validate_api_key():
            return "Error: OpenAI API key not configured"
        
        try:
            response = self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=[
                    {"role": "system", "content": "You are an expert full-stack web developer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', 4000),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            # Track usage
            self.total_tokens_used += response.usage.total_tokens
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"Error generating completion: {str(e)}"
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            'total_tokens_used': self.total_tokens_used,
            'estimated_cost': self.total_tokens_used * 0.00006,  # Rough estimate
            'model': self.model
        }