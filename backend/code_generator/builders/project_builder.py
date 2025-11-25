import os
import logging
from typing import Dict, List, Any
from ..generators import (
    ReactGenerator, VueGenerator, AngularGenerator,
    DjangoGenerator, NodeJSGenerator, FlaskGenerator
)

logger = logging.getLogger(__name__)

class ProjectBuilder:
    """Builds complete full-stack projects by coordinating multiple generators"""
    
    def __init__(self):
        self.generators = {
            'react': ReactGenerator(),
            'vue': VueGenerator(),
            'angular': AngularGenerator(),
            'django': DjangoGenerator(),
            'nodejs': NodeJSGenerator(),
            'flask': FlaskGenerator()
        }
        
        self.supported_stacks = {
            'mern': {'frontend': 'react', 'backend': 'nodejs', 'database': 'mongodb'},
            'mean': {'frontend': 'angular', 'backend': 'nodejs', 'database': 'mongodb'},
            'mevn': {'frontend': 'vue', 'backend': 'nodejs', 'database': 'mongodb'},
            'django_react': {'frontend': 'react', 'backend': 'django', 'database': 'postgresql'},
            'django_vue': {'frontend': 'vue', 'backend': 'django', 'database': 'postgresql'},
            'full_django': {'frontend': 'django', 'backend': 'django', 'database': 'postgresql'}
        }
    
    def build_fullstack_project(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Build a complete full-stack project"""
        try:
            # Determine tech stack
            stack = self._determine_tech_stack(specifications)
            
            # Generate frontend
            frontend_files = self._generate_frontend(stack['frontend'], specifications)
            
            # Generate backend
            backend_files = self._generate_backend(stack['backend'], specifications)
            
            # Generate configuration files
            config_files = self._generate_configuration_files(stack, specifications)
            
            # Generate documentation
            docs_files = self._generate_documentation(stack, specifications)
            
            # Combine all files
            all_files = {}
            all_files.update(self._prefix_files(frontend_files, 'frontend/'))
            all_files.update(self._prefix_files(backend_files, 'backend/'))
            all_files.update(config_files)
            all_files.update(docs_files)
            
            logger.info(f"Generated {len(all_files)} files for {stack['frontend']}-{stack['backend']} stack")
            
            return all_files
            
        except Exception as e:
            logger.error(f"Error building project: {str(e)}")
            return self._get_error_fallback(specifications)
    
    def build_frontend_only(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Build frontend-only project"""
        framework = specifications.get('frontend_framework', 'react')
        generator = self.generators.get(framework)
        
        if not generator:
            raise ValueError(f"Unsupported frontend framework: {framework}")
        
        return generator.generate_project_structure(specifications)
    
    def build_backend_only(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Build backend-only project"""
        framework = specifications.get('backend_framework', 'django')
        generator = self.generators.get(framework)
        
        if not generator:
            raise ValueError(f"Unsupported backend framework: {framework}")
        
        return generator.generate_project_structure(specifications)
    
    def _determine_tech_stack(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Determine the appropriate technology stack based on specifications"""
        # Check if user specified a pre-defined stack
        preferred_stack = specifications.get('preferred_stack')
        if preferred_stack and preferred_stack in self.supported_stacks:
            return self.supported_stacks[preferred_stack]
        
        # Auto-detect based on requirements
        features = specifications.get('features', [])
        complexity = specifications.get('complexity_level', 'medium')
        
        if 'real_time' in features or 'scalability' in specifications:
            return {'frontend': 'react', 'backend': 'nodejs', 'database': 'mongodb'}
        elif 'admin_panel' in features or 'batteries_included' in specifications:
            return {'frontend': 'react', 'backend': 'django', 'database': 'postgresql'}
        elif complexity == 'low':
            return {'frontend': 'vue', 'backend': 'flask', 'database': 'sqlite'}
        else:
            # Default stack
            return {'frontend': 'react', 'backend': 'django', 'database': 'postgresql'}
    
    def _generate_frontend(self, frontend_framework: str, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate frontend code"""
        generator = self.generators.get(frontend_framework)
        if not generator:
            raise ValueError(f"Unsupported frontend framework: {frontend_framework}")
        
        # Enhance specifications for frontend
        frontend_specs = specifications.copy()
        frontend_specs['project_type'] = 'frontend'
        
        return generator.generate_project_structure(frontend_specs)
    
    def _generate_backend(self, backend_framework: str, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate backend code"""
        generator = self.generators.get(backend_framework)
        if not generator:
            raise ValueError(f"Unsupported backend framework: {backend_framework}")
        
        # Enhance specifications for backend
        backend_specs = specifications.copy()
        backend_specs['project_type'] = 'backend'
        
        return generator.generate_project_structure(backend_specs)
    
    def _generate_configuration_files(self, stack: Dict[str, str], specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate project configuration files"""
        config_files = {}
        
        project_name = specifications.get('project_name', 'myapp')
        
        # Docker configuration
        if specifications.get('docker_support', True):
            config_files['Dockerfile'] = self._generate_dockerfile(stack, specifications)
            config_files['docker-compose.yml'] = self._generate_docker_compose(stack, specifications)
        
        # Environment files
        config_files['.env.example'] = self._generate_env_example(stack, specifications)
        
        # Git configuration
        config_files['.gitignore'] = self._generate_gitignore(stack, specifications)
        
        # README
        config_files['README.md'] = self._generate_readme(stack, specifications)
        
        # Deployment files
        if specifications.get('deployment_ready', True):
            config_files.update(self._generate_deployment_files(stack, specifications))
        
        return config_files
    
    def _generate_documentation(self, stack: Dict[str, str], specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate project documentation"""
        docs_files = {}
        
        project_name = specifications.get('project_name', 'myapp')
        
        # API Documentation
        docs_files['docs/API.md'] = f"""# {project_name} API Documentation

## Backend: {stack['backend'].title()}
## Frontend: {stack['frontend'].title()}
## Database: {stack['database'].title()}

## Available Endpoints

### Authentication
- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- POST /api/auth/logout - User logout

### User Management
- GET /api/users/ - List users
- GET /api/users/:id - Get user details
- PUT /api/users/:id - Update user

## Setup Instructions

### Backend Setup
1. Navigate to backend directory
2. Install dependencies
3. Run migrations
4. Start server

### Frontend Setup
1. Navigate to frontend directory
2. Install dependencies
3. Start development server
"""
        
        # Setup guide
        docs_files['docs/SETUP.md'] = f"""# Setup Guide for {project_name}

## Prerequisites
- Node.js (for frontend)
- Python (for backend)
- Database ({stack['database']})

## Installation Steps

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver"""