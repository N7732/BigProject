from typing import Dict, Any
import json

class PromptBuilder:
    """Builds dynamic prompts based on context"""
    
    @staticmethod
    def build_analysis_prompt(user_input: str, context: Dict[str, Any] = None) -> str:
        """Build requirement analysis prompt"""
        base_prompt = """
        Analyze these web development requirements:
        
        {user_input}
        
        {context}
        
        Provide detailed technical specifications.
        """
        
        context_str = ""
        if context:
            context_str = f"Additional context: {json.dumps(context, indent=2)}"
        
        return base_prompt.format(
            user_input=user_input,
            context=context_str
        )
    
    @staticmethod
    def build_generation_prompt(specs: Dict[str, Any], framework: str) -> str:
        """Build code generation prompt"""
        return f"""
        Generate complete {framework} code for these specifications:
        
        {json.dumps(specs, indent=2)}
        
        Create production-ready, well-documented code.
        """