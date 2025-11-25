from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class RequirementSpecs:
    """Data class for requirement specifications"""
    user_input: str
    features: List[str]
    frameworks: Dict[str, str]
    database_requirements: Dict[str, Any]
    api_endpoints: List[str]
    ui_specifications: Dict[str, Any]
    missing_info: List[str]
    complexity_level: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'user_input': self.user_input,
            'features': self.features,
            'frameworks': self.frameworks,
            'database_requirements': self.database_requirements,
            'api_endpoints': self.api_endpoints,
            'ui_specifications': self.ui_specifications,
            'missing_info': self.missing_info,
            'complexity_level': self.complexity_level
        }