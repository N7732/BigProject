import ast
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class Validator:
    def validate_python_code(self, code: str) -> Tuple[bool, List[str]]:
        """Validate Python code syntax"""
        errors = []
        try:
            ast.parse(code)
            return True, errors
        except SyntaxError as e:
            errors.append(f"Syntax error: {str(e)}")
            return False, errors
    
    def validate_json_structure(self, data: Dict, required_fields: List[str]) -> Tuple[bool, List[str]]:
        """Validate JSON structure has required fields"""
        errors = []
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        return len(errors) == 0, errors
    
    def check_security_issues(self, code: str, language: str) -> List[str]:
        """Check for common security issues"""
        security_warnings = []
        
        if language == 'python':
            if 'eval(' in code:
                security_warnings.append('Use of eval() detected - security risk')
            if 'exec(' in code:
                security_warnings.append('Use of exec() detected - security risk')
            if 'os.system(' in code:
                security_warnings.append('Use of os.system() detected - prefer subprocess')
        
        elif language == 'javascript':
            if 'eval(' in code:
                security_warnings.append('Use of eval() detected - security risk')
            if 'innerHTML' in code and 'sanitize' not in code:
                security_warnings.append('Potential XSS vulnerability with innerHTML')
        
        return security_warnings