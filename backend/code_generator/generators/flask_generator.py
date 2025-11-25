from typing import Dict, Any
from .base_generator import BaseGenerator

class FlaskGenerator(BaseGenerator):
    """Flask backend generator"""
    
    def __init__(self):
        super().__init__()
        self.framework_name = "flask"
    
    def generate_project_structure(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        return {
            'app.py': self._generate_app_py(specifications),
            'requirements.txt': 'Flask>=2.0.0'
        }
    
    def generate_main_files(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        return {}
    
    def _generate_app_py(self, specifications: Dict[str, Any]) -> str:
        return """from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello from Flask!'}

if __name__ == '__main__':
    app.run(debug=True)
"""