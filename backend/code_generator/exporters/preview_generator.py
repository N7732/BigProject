import os
import tempfile
import webbrowser
import logging
from typing import Dict, Any, Optional
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

logger = logging.getLogger(__name__)

class PreviewGenerator:
    """Generates live previews of generated projects"""
    
    def __init__(self):
        self.preview_ports = {}
        self.servers = {}
    
    def generate_html_preview(self, files_dict: Dict[str, str]) -> str:
        """Generate an HTML preview of the project"""
        try:
            # Extract HTML files for preview
            html_files = {}
            for file_path, content in files_dict.items():
                if file_path.endswith(('.html', '.htm')):
                    html_files[file_path] = content
            
            if not html_files:
                return self._generate_default_preview(files_dict)
            
            # Create preview HTML
            preview_html = self._create_preview_page(html_files, files_dict)
            return preview_html
            
        except Exception as e:
            logger.error(f"Error generating HTML preview: {str(e)}")
            return self._generate_error_preview(str(e))
    
    def start_live_preview(self, files_dict: Dict[str, str], port: int = 8001) -> str:
        """Start a live preview server"""
        try:
            # Create temporary directory for preview
            temp_dir = tempfile.mkdtemp(prefix='preview_')
            
            # Write files to temporary directory
            for file_path, content in files_dict.items():
                full_path = os.path.join(temp_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Start HTTP server in a thread
            def start_server():
                os.chdir(temp_dir)
                server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
                self.servers[port] = server
                server.serve_forever()
            
            server_thread = threading.Thread(target=start_server, daemon=True)
            server_thread.start()
            
            # Wait for server to start
            time.sleep(1)
            
            preview_url = f'http://localhost:{port}'
            self.preview_ports[port] = temp_dir
            
            logger.info(f"Started live preview at {preview_url}")
            return preview_url
            
        except Exception as e:
            logger.error(f"Error starting live preview: {str(e)}")
            return ""
    
    def stop_live_preview(self, port: int) -> bool:
        """Stop a live preview server"""
        try:
            if port in self.servers:
                self.servers[port].shutdown()
                del self.servers[port]
            
            if port in self.preview_ports:
                # Clean up temporary directory
                import shutil
                shutil.rmtree(self.preview_ports[port], ignore_errors=True)
                del self.preview_ports[port]
            
            logger.info(f"Stopped live preview on port {port}")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping live preview: {str(e)}")
            return False
    
    def open_preview_in_browser(self, preview_url: str) -> bool:
        """Open preview URL in default browser"""
        try:
            webbrowser.open(preview_url)
            logger.info(f"Opened preview in browser: {preview_url}")
            return True
        except Exception as e:
            logger.error(f"Error opening preview in browser: {str(e)}")
            return False
    
    def _create_preview_page(self, html_files: Dict[str, str], all_files: Dict[str, str]) -> str:
        """Create a preview page showing the project structure"""
        file_tree = self._generate_file_tree(all_files)
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Preview</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }}
        .file-tree {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-family: monospace;
        }}
        .preview-section {{
            margin-top: 30px;
        }}
        .file-item {{
            margin: 2px 0;
        }}
        .folder {{
            font-weight: bold;
            color: #1976d2;
        }}
        .file {{
            color: #388e3c;
        }}
        iframe {{
            width: 100%;
            height: 500px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Project Preview</h1>
            <p>Generated automatically by AI Web Generator</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{len(all_files)}</h3>
                <p>Total Files</p>
            </div>
            <div class="stat-card">
                <h3>{len(html_files)}</h3>
                <p>HTML Files</p>
            </div>
            <div class="stat-card">
                <h3>{self._count_file_types(all_files, '.js')}</h3>
                <p>JavaScript Files</p>
            </div>
            <div class="stat-card">
                <h3>{self._count_file_types(all_files, '.css')}</h3>
                <p>CSS Files</p>
            </div>
        </div>
        
        <div class="file-tree">
            <h3>📁 Project Structure</h3>
            <pre>{file_tree}</pre>
        </div>
        
        <div class="preview-section">
            <h3>👀 Live Preview</h3>
            <p>Select an HTML file to preview:</p>
            <select id="fileSelector" onchange="updatePreview()">
                <option value="">Select a file...</option>
                {"".join([f'<option value="{path}">{path}</option>' for path in html_files.keys()])}
            </select>
            
            <div style="margin-top: 15px;">
                <iframe id="previewFrame" src="about:blank"></iframe>
            </div>
        </div>
    </div>
    
    <script>
        function updatePreview() {{
            const selector = document.getElementById('fileSelector');
            const frame = document.getElementById('previewFrame');
            const selectedFile = selector.value;
            
            if (selectedFile) {{
                frame.src = selectedFile;
            }} else {{
                frame.src = 'about:blank';
            }}
        }}
    </script>
</body>
</html>
"""
    
    def _generate_file_tree(self, files_dict: Dict[str, str]) -> str:
        """Generate a text-based file tree"""
        tree_structure = {}
        
        for file_path in files_dict.keys():
            parts = file_path.split('/')
            current = tree_structure
            
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        
        def build_tree(node, prefix="", is_last=True):
            lines = []
            items = list(node.items())
            
            for i, (name, children) in enumerate(items):
                is_last_item = (i == len(items) - 1)
                connector = "└── " if is_last_item else "├── "
                
                if children:  # It's a folder
                    lines.append(f"{prefix}{connector}📁 {name}/")
                    new_prefix = prefix + ("    " if is_last_item else "│   ")
                    lines.extend(build_tree(children, new_prefix, is_last_item))
                else:  # It's a file
                    lines.append(f"{prefix}{connector}📄 {name}")
            
            return lines
        
        tree_lines = build_tree(tree_structure)
        return "\n".join(tree_lines)
    
    def _count_file_types(self, files_dict: Dict[str, str], extension: str) -> int:
        """Count files of specific type"""
        return sum(1 for file_path in files_dict.keys() if file_path.endswith(extension))
    
    def _generate_default_preview(self, files_dict: Dict[str, str]) -> str:
        """Generate default preview when no HTML files found"""
        file_tree = self._generate_file_tree(files_dict)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Code Preview</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        .file-tree {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Generated Code Preview</h1>
    <p>This project contains {len(files_dict)} files.</p>
    
    <div class="file-tree">
        <h3>Project Structure:</h3>
        <pre>{file_tree}</pre>
    </div>
    
    <h3>File Contents:</h3>
    <div>
        {"".join([f'<details><summary>{path}</summary><pre>{content[:500]}...</pre></details>' 
          for path, content in list(files_dict.items())[:10]])}
    </div>
</body>
</html>
"""
    
    def _generate_error_preview(self, error_message: str) -> str:
        """Generate error preview page"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Preview Error</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 40px; text-align: center; }}
        .error {{ color: #d32f2f; background: #ffebee; padding: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>❌ Preview Generation Error</h1>
    <div class="error">
        <h3>Error Details:</h3>
        <p>{error_message}</p>
    </div>
    <p>Please try generating the project again.</p>
</body>
</html>
"""