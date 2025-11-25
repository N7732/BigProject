from typing import Dict, Any
from .base_generator import BaseGenerator

class NodeJSGenerator(BaseGenerator):
    """Node.js backend generator"""
    
    def __init__(self):
        super().__init__()
        self.framework_name = "nodejs"
    
    def generate_project_structure(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        return {
            'package.json': self._generate_package_json(specifications),
            'app.js': '// Node.js application',
            'routes/api.js': '// API routes'
        }
    
    def generate_main_files(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        return {}
    
    def _generate_package_json(self, specifications: Dict[str, Any]) -> str:
        return """{
  "name": "nodejs-app",
  "dependencies": {
    "express": "^4.18.0"
  }
}"""