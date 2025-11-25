from dataclasses import dataclass
from typing import Dict, List

@dataclass
class GenerationResult:
    """Data class for code generation results"""
    success: bool
    code_files: Dict[str, str]  # filename -> content
    warnings: List[str]
    errors: List[str]
    total_files: int
    main_components: List[str]
    
    def add_file(self, filename: str, content: str):
        """Add a generated file to results"""
        self.code_files[filename] = content
        self.total_files += 1
    
    def add_warning(self, warning: str):
        """Add a warning message"""
        self.warnings.append(warning)
    
    def add_error(self, error: str):
        """Add an error message"""
        self.errors.append(error)
        self.success = False