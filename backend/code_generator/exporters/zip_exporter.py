import os
import zipfile
import tempfile
import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class ZipExporter:
    """Handles exporting generated projects to ZIP files"""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def export_to_zip(self, files_dict: Dict[str, str], project_name: str) -> str:
        """Export file dictionary to a ZIP file"""
        try:
            # Create a temporary directory for the project
            with tempfile.TemporaryDirectory() as temp_dir:
                project_path = os.path.join(temp_dir, project_name)
                
                # Create all files in the temporary directory
                self._create_files_structure(project_path, files_dict)
                
                # Create ZIP file
                zip_filename = f"{project_name}.zip"
                zip_path = os.path.join(self.temp_dir, zip_filename)
                
                self._create_zip_from_directory(project_path, zip_path)
                
                logger.info(f"Exported project to {zip_path} with {len(files_dict)} files")
                return zip_path
                
        except Exception as e:
            logger.error(f"Error exporting to ZIP: {str(e)}")
            return ""
    
    def export_to_directory(self, files_dict: Dict[str, str], output_dir: str) -> bool:
        """Export file dictionary to a directory structure"""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Create all files
            self._create_files_structure(output_dir, files_dict)
            
            logger.info(f"Exported project to {output_dir} with {len(files_dict)} files")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to directory: {str(e)}")
            return False
    
    def _create_files_structure(self, base_path: str, files_dict: Dict[str, str]) -> None:
        """Create the complete file structure from dictionary"""
        for file_path, content in files_dict.items():
            full_path = os.path.join(base_path, file_path)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write file content
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def _create_zip_from_directory(self, source_dir: str, zip_path: str) -> None:
        """Create ZIP file from directory"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    def get_zip_info(self, zip_path: str) -> Dict[str, Any]:
        """Get information about a ZIP file"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                file_list = zipf.namelist()
                
                return {
                    'file_count': len(file_list),
                    'total_size': sum(zipf.getinfo(f).file_size for f in file_list),
                    'files': file_list,
                    'compressed_size': os.path.getsize(zip_path)
                }
        except Exception as e:
            logger.error(f"Error reading ZIP info: {str(e)}")
            return {}
    
    def create_download_response(self, zip_path: str, project_name: str) -> Dict[str, Any]:
        """Create download response data for the frontend"""
        zip_info = self.get_zip_info(zip_path)
        
        return {
            'download_url': f'/api/download/{project_name}.zip',
            'file_name': f'{project_name}.zip',
            'file_size': zip_info.get('total_size', 0),
            'file_count': zip_info.get('file_count', 0),
            'project_name': project_name,
            'created_at': os.path.getctime(zip_path)
        }
    
    def cleanup_old_exports(self, max_age_hours: int = 24) -> int:
        """Clean up old export files"""
        try:
            deleted_count = 0
            current_time = os.path.getctime(__file__)  # Reference time
            
            for file in os.listdir(self.temp_dir):
                if file.endswith('.zip'):
                    file_path = os.path.join(self.temp_dir, file)
                    file_age = current_time - os.path.getctime(file_path)
                    
                    # Convert hours to seconds
                    if file_age > (max_age_hours * 3600):
                        os.remove(file_path)
                        deleted_count += 1
                        logger.info(f"Cleaned up old export: {file}")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up exports: {str(e)}")
            return 0