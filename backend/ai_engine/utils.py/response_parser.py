import json
import re
from typing import Dict, Any, List

class ResponseParser:
    """Parses AI responses into structured data"""
    
    @staticmethod
    def extract_json_from_response(response: str) -> Dict[str, Any]:
        """Extract JSON from AI response"""
        try:
            # Try to find JSON in code blocks
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Try to find JSON without code blocks
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            
            return {}
        except json.JSONDecodeError:
            return {}
    
    @staticmethod
    def extract_code_blocks(response: str) -> Dict[str, str]:
        """Extract code blocks from response"""
        code_blocks = {}
        
        # Pattern for code blocks with language specification
        pattern = r'```(\w+)\n(.*?)\n```'
        matches = re.findall(pattern, response, re.DOTALL)
        
        for lang, code in matches:
            code_blocks[f"{lang}_code"] = code.strip()
        
        return code_blocks
    
    @staticmethod
    def parse_clarification_questions(response: str) -> List[str]:
        """Parse clarification questions from response"""
        questions = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for numbered questions or bullet points
            if re.match(r'^(\d+\.|\-|\•)\s+.+\?$', line):
                question = re.sub(r'^(\d+\.|\-|\•)\s+', '', line)
                questions.append(question)
        
        return questions