from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ProjectSpecifications:
    """Data class for complete project specifications"""
    project_name: str
    description: str
    frontend_framework: str
    backend_framework: str
    database_system: str
    authentication_method: str
    features: List[str]
    models: List[Dict[str, Any]]
    api_endpoints: List[Dict[str, Any]]
    ui_components: List[Dict[str, Any]]
    deployment_platform: str
    
    def is_complete(self) -> bool:
        """Check if specifications are complete enough for code generation"""
        required_fields = [
            self.frontend_framework,
            self.backend_framework, 
            self.database_system,
            self.authentication_method
        ]
        return all(required_fields) and len(self.features) > 0