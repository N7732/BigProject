from typing import Dict, Any
from .base_generator import BaseGenerator

class AngularGenerator(BaseGenerator):
    """Angular frontend generator"""
    
    def __init__(self):
        super().__init__()
        self.framework_name = "angular"
    
    def generate_project_structure(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate Angular project structure"""
        return {
            'package.json': self._generate_package_json(specifications),
            'src/main.ts': '// Angular main file',
            'angular.json': '// Angular configuration'
        }
    
    def generate_main_files(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        return {}
    
    def _generate_package_json(self, specifications: Dict[str, Any]) -> str:
        return """{
  "name": "angular-app",
  "dependencies": {
    "@angular/core": "^16.0.0"
  }
}"""