from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class BaseGenerator(ABC):
    """Abstract base class for all code generators"""
    
    def __init__(self):
        self.framework_name = "base"
        self.supported_features = []
    
    @abstractmethod
    def generate_project_structure(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate complete project structure"""
        pass
    
    @abstractmethod
    def generate_main_files(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate main application files"""
        pass
    
    def generate_config_files(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate configuration files"""
        return {}
    
    def generate_documentation(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate documentation files"""
        return {}
    
    def validate_specifications(self, specifications: Dict[str, Any]) -> bool:
        """Validate if specifications are compatible with this generator"""
        required_fields = ['project_name', 'features', 'frameworks']
        return all(field in specifications for field in required_fields)
    
    def get_supported_features(self) -> List[str]:
        """Get list of supported features"""
        return self.supported_features