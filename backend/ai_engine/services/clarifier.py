from typing import List, Dict, Any
from ..clients.openai_client import OpenAIClient
from ..prompts.clarification_prompts import CLARIFICATION_PROMPT

class Clarifier:
    def __init__(self):
        self.ai_client = OpenAIClient()
    
    def generate_clarifying_questions(self, current_specs: Dict[str, Any]) -> List[str]:
        """Generate questions to clarify missing requirements"""
        prompt = CLARIFICATION_PROMPT.format(current_specs=current_specs)
        
        response = self.ai_client.generate_completion(prompt)
        
        return self._parse_questions_response(response)
    
    def _parse_questions_response(self, response: str) -> List[str]:
        """Parse AI response into list of questions"""
        questions = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or '?' in line):
                # Clean up the question
                question = line.lstrip('-• ').strip()
                if question:
                    questions.append(question)
        
        # Default questions if parsing fails
        if not questions:
            questions = [
                "What authentication method would you prefer?",
                "Do you have any specific UI framework in mind?",
                "What's your preferred database system?",
                "Any specific features you want to prioritize?"
            ]
        
        return questions[:5]  # Return max 5 questions