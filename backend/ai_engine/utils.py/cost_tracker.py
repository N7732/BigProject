import time
from typing import Dict, Any, List

class CostTracker:
    """Tracks AI API usage and costs"""
    
    def __init__(self):
        self.requests = []
        self.total_cost = 0.0
    
    def log_request(self, provider: str, model: str, tokens: int, cost: float):
        """Log an API request"""
        request_data = {
            'timestamp': time.time(),
            'provider': provider,
            'model': model,
            'tokens': tokens,
            'cost': cost
        }
        self.requests.append(request_data)
        self.total_cost += cost
    
    def get_daily_usage(self) -> Dict[str, Any]:
        """Get today's usage statistics"""
        today = time.time() - 86400  # 24 hours ago
        
        today_requests = [req for req in self.requests if req['timestamp'] > today]
        today_cost = sum(req['cost'] for req in today_requests)
        today_tokens = sum(req['tokens'] for req in today_requests)
        
        return {
            'requests_today': len(today_requests),
            'tokens_today': today_tokens,
            'cost_today': today_cost,
            'average_cost_per_request': today_cost / len(today_requests) if today_requests else 0
        }
    
    def get_total_usage(self) -> Dict[str, Any]:
        """Get total usage statistics"""
        return {
            'total_requests': len(self.requests),
            'total_cost': self.total_cost,
            'total_tokens': sum(req['tokens'] for req in self.requests)
        }