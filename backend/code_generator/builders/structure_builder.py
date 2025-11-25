import os
import zipfile
import tempfile
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class StructureBuilder:
    """Builds and manages project folder structures"""
    
    def __init__(self):
        self.common_structures = {
            'react': {
                'folders': [
                    'src/components',
                    'src/pages', 
                    'src/hooks',
                    'src/utils',
                    'src/styles',
                    'public',
                    'build'
                ],
                'files': [
                    'src/App.js',
                    'src/index.js',
                    'public/index.html',
                    'package.json'
                ]
            },
            'django': {
                'folders': [
                    'project_name/settings',
                    'apps/core',
                    'apps/core/migrations',
                    'apps/core/static',
                    'apps/core/templates',
                    'static',
                    'media',
                    'templates'
                ],
                'files': [
                    'manage.py',
                    'project_name/__init__.py',
                    'project_name/settings/__init__.py',
                    'project_name/settings/base.py',
                    'project_name/urls.py',
                    'project_name/wsgi.py',
                    'requirements.txt'
                ]
            },
            'fullstack': {
                'folders': [
                    'frontend/src',
                    'frontend/public',
                    'backend/apps',
                    'backend/static',
                    'docs',
                    'scripts'
                ]
            }
        }
    
    def create_folder_structure(self, base_path: str, structure: Dict[str, List[str]]) -> bool:
        """Create a complete folder structure"""
        try:
            # Create base directory
            os.makedirs(base_path, exist_ok=True)
            
            # Create folders
            for folder_type, folders in structure.items():
                for folder in folders:
                    full_path = os.path.join(base_path, folder)
                    os.makedirs(full_path, exist_ok=True)
                    logger.debug(f"Created folder: {full_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating folder structure: {str(e)}")
            return False
    
    def get_structure_for_framework(self, framework: str, project_name: str = None) -> Dict[str, List[str]]:
        """Get predefined structure for a framework"""
        structure = self.common_structures.get(framework, {}).copy()
        
        if project_name and framework == 'django':
            # Replace placeholder with actual project name
            structure['folders'] = [
                folder.replace('project_name', project_name) 
                for folder in structure.get('folders', [])
            ]
            structure['files'] = [
                file.replace('project_name', project_name)
                for file in structure.get('files', [])
            ]
        
        return structure
    
    def create_project_structure(self, project_type: str, project_name: str, base_path: str = ".") -> Dict[str, Any]:
        """Create a complete project structure"""
        try:
            project_path = os.path.join(base_path, project_name)
            
            # Get structure definition
            structure = self.get_structure_for_framework(project_type, project_name)
            
            # Create folders
            if not self.create_folder_structure(project_path, structure):
                return {'success': False, 'error': 'Failed to create folder structure'}
            
            # Create empty files
            files_created = []
            for file_path in structure.get('files', []):
                full_file_path = os.path.join(project_path, file_path)
                
                # Ensure parent directory exists
                os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
                
                # Create empty file
                with open(full_file_path, 'w') as f:
                    f.write(f"# {os.path.basename(file_path)}\n# Auto-generated file\n")
                files_created.append(file_path)
            
            result = {
                'success': True,
                'project_path': project_path,
                'folders_created': structure.get('folders', []),
                'files_created': files_created,
                'total_items': len(structure.get('folders', [])) + len(files_created)
            }
            
            logger.info(f"Created project structure at {project_path} with {result['total_items']} items")
            return result
            
        except Exception as e:
            logger.error(f"Error creating project structure: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_zip_structure(self, files_dict: Dict[str, str], zip_filename: str) -> str:
        """Create a ZIP file from file dictionary"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path, content in files_dict.items():
                        # Ensure proper path formatting
                        clean_path = file_path.lstrip('/').lstrip('\\')
                        
                        # Add file to zip
                        zipf.writestr(clean_path, content)
                
                # Move to final location
                final_path = zip_filename
                os.rename(temp_zip.name, final_path)
                
                logger.info(f"Created ZIP file: {final_path} with {len(files_dict)} files")
                return final_path
                
        except Exception as e:
            logger.error(f"Error creating ZIP file: {str(e)}")
            return ""
    
    def analyze_existing_structure(self, path: str) -> Dict[str, Any]:
        """Analyze an existing project structure"""
        try:
            if not os.path.exists(path):
                return {'error': 'Path does not exist'}
            
            structure = {
                'path': path,
                'folders': [],
                'files': [],
                'total_size': 0,
                'file_types': {},
                'depth': 0
            }
            
            for root, dirs, files in os.walk(path):
                # Calculate depth
                current_depth = root.replace(path, '').count(os.sep)
                structure['depth'] = max(structure['depth'], current_depth)
                
                # Add folders
                for dir_name in dirs:
                    folder_path = os.path.join(root, dir_name)
                    structure['folders'].append(folder_path)
                
                # Add files and analyze
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    structure['files'].append(file_path)
                    
                    # Get file size
                    try:
                        file_size = os.path.getsize(file_path)
                        structure['total_size'] += file_size
                    except OSError:
                        file_size = 0
                    
                    # Count file types
                    file_ext = os.path.splitext(file_name)[1].lower()
                    structure['file_types'][file_ext] = structure['file_types'].get(file_ext, 0) + 1
            
            structure['total_folders'] = len(structure['folders'])
            structure['total_files'] = len(structure['files'])
            
            return structure
            
        except Exception as e:
            logger.error(f"Error analyzing structure: {str(e)}")
            return {'error': str(e)}
    
    def validate_structure(self, structure: Dict[str, List[str]]) -> Dict[str, Any]:
        """Validate a project structure definition"""
        issues = []
        warnings = []
        
        folders = structure.get('folders', [])
        files = structure.get('files', [])
        
        # Check for duplicate entries
        all_items = folders + files
        duplicates = set([x for x in all_items if all_items.count(x) > 1])
        if duplicates:
            issues.append(f"Duplicate entries found: {list(duplicates)}")
        
        # Check for invalid characters in paths
        invalid_chars = '<>:"|?*'
        for item in all_items:
            for char in invalid_chars:
                if char in item:
                    issues.append(f"Invalid character '{char}' in path: {item}")
                    break
        
        # Check for absolute paths (should be relative)
        for item in all_items:
            if os.path.isabs(item):
                warnings.append(f"Absolute path detected (should be relative): {item}")
        
        # Check for very deep nesting
        for folder in folders:
            depth = folder.count('/') + folder.count('\\')
            if depth > 10:
                warnings.append(f"Very deep folder nesting: {folder}")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'total_folders': len(folders),
            'total_files': len(files)
        }
    
    def generate_tree_diagram(self, files_dict: Dict[str, str]) -> str:
        """Generate a tree diagram from file dictionary"""
        tree_lines = ["📁 project/"]
        
        # Organize files into tree structure
        tree_structure = {}
        for file_path in files_dict.keys():
            parts = file_path.split('/')
            current_level = tree_structure
            
            for part in parts[:-1]:  # All but the last part (filename)
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            
            # Add file to current level
            filename = parts[-1]
            if 'files' not in current_level:
                current_level['files'] = []
            current_level['files'].append(filename)
        
        # Recursive function to build tree
        def build_tree(node, prefix="", is_last=True):
            nonlocal tree_lines
            
            if not node:
                return
            
            # Get folders and files
            folders = [k for k in node.keys() if k != 'files']
            files = node.get('files', [])
            
            all_items = sorted(folders) + sorted(files)
            
            for i, item in enumerate(all_items):
                is_last_item = (i == len(all_items) - 1)
                connector = "└── " if is_last_item else "├── "
                
                if item in folders:  # It's a folder
                    tree_lines.append(f"{prefix}{connector}📁 {item}/")
                    new_prefix = prefix + ("    " if is_last_item else "│   ")
                    build_tree(node[item], new_prefix, is_last_item)
                else:  # It's a file
                    tree_lines.append(f"{prefix}{connector}📄 {item}")
        
        build_tree(tree_structure)
        return "\n".join(tree_lines)
    
    def calculate_project_size(self, files_dict: Dict[str, str]) -> Dict[str, Any]:
        """Calculate size statistics for generated project"""
        total_size = 0
        file_count_by_type = {}
        
        for file_path, content in files_dict.items():
            file_size = len(content.encode('utf-8'))
            total_size += file_size
            
            # Get file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            file_count_by_type[file_ext] = file_count_by_type.get(file_ext, 0) + 1
        
        return {
            'total_files': len(files_dict),
            'total_size_bytes': total_size,
            'total_size_kb': round(total_size / 1024, 2),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'files_by_type': file_count_by_type,
            'average_file_size': round(total_size / len(files_dict), 2) if files_dict else 0
        }