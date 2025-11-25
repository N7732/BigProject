import json
import logging
from typing import Dict, List, Any
from ..clients.openai_client import OpenAIClient
from ..prompts.analysis_prompts import REQUIREMENT_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)

class RequirementAnalyzer:
    def __init__(self):
        self.ai_client = OpenAIClient()
    
    def analyze_requirements(self, user_input: str) -> Dict[str, Any]:
        """Analyze user requirements and extract specifications"""
        try:
            prompt = REQUIREMENT_ANALYSIS_PROMPT.format(user_input=user_input)
            
            response = self.ai_client.generate_completion(prompt)
            
            return self._parse_analysis_response(response)
        except Exception as e:
            logger.error(f"Error analyzing requirements: {str(e)}")
            return self._get_default_specs()
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured specifications"""
        try:
            # Try to parse as JSON first
            if response.strip().startswith('{'):
                return json.loads(response)
            
            # Fallback: extract key information
            specs = {
                'features': self._extract_features(response),
                'frameworks': self._extract_frameworks(response),
                'database_requirements': self._extract_database_info(response),
                'api_endpoints': self._extract_endpoints(response),
                'ui_specifications': self._extract_ui_specs(response),
                'missing_info': self._extract_missing_info(response),
                'complexity_level': self._assess_complexity(response)
            }
            return specs
        except json.JSONDecodeError:
            return self._get_default_specs()
    
    def _extract_features(self, response: str) -> List[str]:
        """Extract features from AI response"""
        # Implementation for feature extraction
        return ['authentication', 'user_dashboard']  # Default
    
    def _extract_frameworks(self, response: str) -> Dict[str, str]:
        """Extract suggested frameworks"""
        return {'frontend': 'react', 'backend': 'django'}
    
    def _extract_database_info(self, response: str) -> Dict[str, Any]:
        """Extract database requirements"""
        return {'type': 'postgresql', 'models': ['User', 'Profile']}
    
    def _extract_endpoints(self, response: str) -> List[str]:
        """Extract API endpoints"""
        return ['/api/auth/', '/api/users/']
    
    def _extract_ui_specs(self, response: str) -> Dict[str, Any]:
        """Extract UI specifications"""
        return {'style': 'modern', 'responsive': True}
    
    def _extract_missing_info(self, response: str) -> List[str]:
        """Extract missing information"""
        return ['authentication method', 'database preferences']
    
    def _assess_complexity(self, response: str) -> str:
        """Assess project complexity"""
        return 'medium'
    
    def _get_default_specs(self) -> Dict[str, Any]:
        """Return default specifications on error"""
        return {
            'features': ['basic_crud'],
            'frameworks': {'frontend': 'react', 'backend': 'django'},
            'database_requirements': {'type': 'sqlite', 'models': []},
            'api_endpoints': [],
            'ui_specifications': {'style': 'basic', 'responsive': True},
            'missing_info': ['detailed requirements'],
            'complexity_level': 'low'
        }