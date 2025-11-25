import hashlib
import json
from typing import Any, Optional

class CacheManager:
    """Manages caching of AI responses to reduce API calls"""
    
    def __init__(self):
        self.cache = {}
    
    def get_cache_key(self, prompt: str, context: dict[str, Any] = None) -> str:
        """Generate cache key from prompt and context"""
        key_data = prompt
        if context:
            key_data += json.dumps(context, sort_keys=True)
        
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get_cached_response(self, prompt: str, context: dict[str, Any] = None) -> Optional[str]:
        """Get cached response if exists"""
        cache_key = self.get_cache_key(prompt, context)
        return self.cache.get(cache_key)
    
    def cache_response(self, prompt: str, response: str, context: dict[str, Any] = None):
        """Cache AI response"""
        cache_key = self.get_cache_key(prompt, context)
        self.cache[cache_key] = response
    
    def clear_cache(self):
        """Clear all cached responses"""
        self.cache.clear()