import logging
from typing import Dict, Any
from ..clients.openai_client import OpenAIClient
from ..prompts.generation_prompts import CODE_GENERATION_PROMPT

logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self):
        self.ai_client = OpenAIClient()
    
    def generate_code_snippets(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate code snippets based on specifications"""
        try:
            prompt = CODE_GENERATION_PROMPT.format(specifications=specifications)
            
            response = self.ai_client.generate_completion(prompt)
            
            return self._parse_code_response(response)
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            return self._get_default_code()
    
    def _parse_code_response(self, response: str) -> Dict[str, str]:
        """Parse AI response into code snippets"""
        # Extract different code sections from response
        code_snippets = {}
        
        # Simple parsing - in reality, you'd use more sophisticated parsing
        lines = response.split('\n')
        current_section = None
        current_code = []
        
        for line in lines:
            if line.startswith('**') and line.endswith('**'):
                if current_section and current_code:
                    code_snippets[current_section] = '\n'.join(current_code)
                current_section = line.strip('*').strip().lower().replace(' ', '_')
                current_code = []
            else:
                current_code.append(line)
        
        if current_section and current_code:
            code_snippets[current_section] = '\n'.join(current_code)
            
        return code_snippets
    
    def _get_default_code(self) -> Dict[str, str]:
        """Return default code on error"""
        return {
            'frontend_app_js': '// Default React app\nfunction App() { return <div>Hello World</div>; }',
            'backend_views': '# Default Django views\nfrom django.http import JsonResponse\n\ndef home(request): return JsonResponse({"status": "ok"})'
        }