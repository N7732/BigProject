import os
import logging
import subprocess
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DeploymentHelper:
    """Provides deployment assistance and instructions"""
    
    def __init__(self):
        self.deployment_platforms = {
            'vercel': self._get_vercel_instructions,
            'netlify': self._get_netlify_instructions,
            'heroku': self._get_heroku_instructions,
            'railway': self._get_railway_instructions,
            'digitalocean': self._get_digitalocean_instructions,
            'aws': self._get_aws_instructions
        }
    
    def generate_deployment_instructions(self, project_type: str, platform: str) -> Dict[str, Any]:
        """Generate deployment instructions for specific platform"""
        if platform not in self.deployment_platforms:
            return self._get_generic_instructions(project_type)
        
        try:
            instructions = self.deployment_platforms[platform](project_type)
            return instructions
        except Exception as e:
            logger.error(f"Error generating {platform} instructions: {str(e)}")
            return self._get_generic_instructions(project_type)
    
    def check_deployment_readiness(self, files_dict: Dict[str, str]) -> Dict[str, Any]:
        """Check if project is ready for deployment"""
        checks = {
            'has_package_json': False,
            'has_requirements_txt': False,
            'has_env_example': False,
            'has_readme': False,
            'has_gitignore': False,
            'missing_files': []
        }
        
        required_files = {
            'package.json': 'Frontend dependencies',
            'requirements.txt': 'Backend dependencies',
            '.env.example': 'Environment configuration',
            'README.md': 'Documentation',
            '.gitignore': 'Git configuration'
        }
        
        for required_file, description in required_files.items():
            if any(required_file in file_path for file_path in files_dict.keys()):
                key = f"has_{required_file.replace('.', '_').replace('-', '_')}"
                if key in checks:
                    checks[key] = True
            else:
                checks['missing_files'].append(f"{required_file} ({description})")
        
        checks['is_ready'] = len(checks['missing_files']) == 0
        checks['score'] = sum(1 for key, value in checks.items() 
                            if key.startswith('has_') and value) / 5 * 100
        
        return checks
    
    def generate_deployment_script(self, platform: str, project_type: str) -> str:
        """Generate deployment script for specific platform"""
        if platform == 'vercel':
            return self._generate_vercel_script(project_type)
        elif platform == 'heroku':
            return self._generate_heroku_script(project_type)
        elif platform == 'digitalocean':
            return self._generate_digitalocean_script(project_type)
        else:
            return self._generate_generic_deployment_script(project_type)
    
    def _get_vercel_instructions(self, project_type: str) -> Dict[str, Any]:
        """Get Vercel deployment instructions"""
        return {
            'platform': 'Vercel',
            'description': 'Serverless deployment platform for frontend and serverless functions',
            'steps': [
                '1. Install Vercel CLI: npm i -g vercel',
                '2. Login to Vercel: vercel login',
                '3. Deploy: vercel --prod',
                '4. For continuous deployment, connect your GitHub repository'
            ],
            'requirements': [
                'package.json file',
                'Build script in package.json',
                'Proper start script for serverless functions'
            ],
            'config_file': 'vercel.json',
            'config_example': self._get_vercel_config_example(project_type),
            'pros': [
                'Free tier available',
                'Automatic HTTPS',
                'Global CDN',
                'Continuous deployment'
            ],
            'cons': [
                'Serverless functions have limits',
                'Not ideal for long-running processes'
            ]
        }
    
    def _get_netlify_instructions(self, project_type: str) -> Dict[str, Any]:
        """Get Netlify deployment instructions"""
        return {
            'platform': 'Netlify',
            'description': 'Static site hosting with serverless functions',
            'steps': [
                '1. Build your project: npm run build',
                '2. Drag and drop build folder to Netlify',
                '3. Or connect GitHub repository for auto-deployment',
                '4. Configure environment variables in Netlify dashboard'
            ],
            'requirements': [
                'Build output directory',
                'Netlify.toml for configuration'
            ],
            'config_file': 'netlify.toml',
            'config_example': self._get_netlify_config_example(project_type),
            'pros': [
                'Easy drag-and-drop deployment',
                'Free tier',
                'Forms handling',
                'Identity service'
            ],
            'cons': [
                'Limited serverless functions',
                'Build time limits'
            ]
        }
    
    def _get_heroku_instructions(self, project_type: str) -> Dict[str, Any]:
        """Get Heroku deployment instructions"""
        return {
            'platform': 'Heroku',
            'description': 'Platform as a Service for full-stack applications',
            'steps': [
                '1. Install Heroku CLI',
                '2. Login: heroku login',
                '3. Create app: heroku create',
                '4. Set environment variables: heroku config:set KEY=value',
                '5. Deploy: git push heroku main'
            ],
            'requirements': [
                'Procfile',
                'requirements.txt (for Python)',
                'package.json (for Node.js)'
            ],
            'config_file': 'Procfile',
            'config_example': self._get_heroku_config_example(project_type),
            'pros': [
                'Easy deployment process',
                'Add-ons ecosystem',
                'Good for full-stack apps'
            ],
            'cons': [
                'Dyno hours limited on free tier',
                'Can get expensive for high traffic'
            ]
        }
    
    def _get_railway_instructions(self, project_type: str) -> Dict[str, Any]:
        """Get Railway deployment instructions"""
        return {
            'platform': 'Railway',
            'description': 'Modern deployment platform with great developer experience',
            'steps': [
                '1. Connect GitHub repository',
                '2. Railway automatically detects framework',
                '3. Set environment variables',
                '4. Deploys automatically on git push'
            ],
            'requirements': [
                'GitHub repository',
                'Proper package.json or requirements.txt'
            ],
            'config_file': 'railway.toml (optional)',
            'config_example': self._get_railway_config_example(project_type),
            'pros': [
                'Great free tier',
                'Easy GitHub integration',
                'Automatic deployments',
                'Good documentation'
            ],
            'cons': [
                'Newer platform',
                'Fewer integrations than Heroku'
            ]
        }
    
    def _get_digitalocean_instructions(self, project_type: str) -> Dict[str, Any]:
        """Get DigitalOcean deployment instructions"""
        return {
            'platform': 'DigitalOcean',
            'description': 'VPS hosting with Droplets or App Platform',
            'steps': [
                '1. Create Droplet or App Platform app',
                '2. Connect GitHub repository',
                '3. Configure build and run commands',
                '4. Set environment variables'
            ],
            'requirements': [
                'Dockerfile or build commands',
                'Proper startup configuration'
            ],
            'config_file': 'app.yaml (for App Platform)',
            'config_example': self._get_digitalocean_config_example(project_type),
            'pros': [
                'Predictable pricing',
                'Good performance',
                'Multiple hosting options'
            ],
            'cons': [
                'More configuration required',
                'Not as simple as PaaS'
            ]
        }
    
    def _get_aws_instructions(self, project_type: str) -> Dict[str, Any]:
        """Get AWS deployment instructions"""
        return {
            'platform': 'AWS',
            'description': 'Cloud infrastructure with multiple service options',
            'steps': [
                '1. Frontend: S3 + CloudFront for static hosting',
                '2. Backend: Elastic Beanstalk or ECS for applications',
                '3. Database: RDS or DynamoDB',
                '4. Configure IAM roles and security groups'
            ],
            'requirements': [
                'AWS account',
                'IAM configuration',
                'Proper security settings'
            ],
            'config_file': 'Various AWS configuration files',
            'config_example': self._get_aws_config_example(project_type),
            'pros': [
                'Highly scalable',
                'Extensive services',
                'Enterprise features'
            ],
            'cons': [
                'Complex setup',
                'Cost management required',
                'Steep learning curve'
            ]
        }
    
    def _get_generic_instructions(self, project_type: str) -> Dict[str, Any]:
        """Get generic deployment instructions"""
        return {
            'platform': 'Generic',
            'description': 'General deployment instructions',
            'steps': [
                '1. Build your project: npm run build (frontend)',
                '2. Set up production database',
                '3. Configure environment variables',
                '4. Set up web server (Nginx/Apache)',
                '5. Configure domain and SSL'
            ],
            'requirements': [
                'Production build',
                'Environment configuration',
                'Web server setup'
            ],
            'config_file': 'Various configuration files',
            'pros': [
                'Full control',
                'Custom configuration'
            ],
            'cons': [
                'More setup required',
                'Manual maintenance'
            ]
        }
    
    def _get_vercel_config_example(self, project_type: str) -> str:
        """Get Vercel config example"""
        if project_type == 'react':
            return """{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "build" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/build/$1"
    }
  ]
}"""
        else:
            return """{
  "version": 2,
  "builds": [
    {
      "src": "*.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.js"
    }
  ]
}"""
    
    def _get_netlify_config_example(self, project_type: str) -> str:
        """Get Netlify config example"""
        return """[build]
  publish = "build"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200"""
    
    def _get_heroku_config_example(self, project_type: str) -> str:
        """Get Heroku config example"""
        if 'django' in project_type:
            return "web: gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT"
        elif 'node' in project_type:
            return "web: node index.js"
        else:
            return "web: python app.py"
    
    def _get_railway_config_example(self, project_type: str) -> str:
        """Get Railway config example"""
        return """[build]
builder = "nixpacks"

[deploy]
startCommand = "python manage.py runserver 0.0.0.0:$PORT"

[environments.production]
NODE_ENV = "production"
DEBUG = "false" """
    
    def _get_digitalocean_config_example(self, project_type: str) -> str:
        """Get DigitalOcean config example"""
        return """name: my-app
services:
- name: web
  source_dir: /
  github:
    branch: main
    deploy_on_push: true
  run_command: python manage.py runserver 0.0.0.0:$PORT
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs"""
    
    def _get_aws_config_example(self, project_type: str) -> str:
        """Get AWS config example"""
        return """# Elastic Beanstalk .ebextensions configuration
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: myproject:application
  aws:elasticbeanstalk:application:environment:
    DEBUG: false"""
    
    def _generate_vercel_script(self, project_type: str) -> str:
        """Generate Vercel deployment script"""
        return """#!/bin/bash
# Vercel Deployment Script

echo "🚀 Deploying to Vercel..."

# Install Vercel CLI if not exists
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

# Deploy
vercel --prod

echo "✅ Deployment complete!" """
    
    def _generate_heroku_script(self, project_type: str) -> str:
        """Generate Heroku deployment script"""
        return """#!/bin/bash
# Heroku Deployment Script

echo "🚀 Deploying to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not installed. Please install it first."
    exit 1
fi

# Login (if not already logged in)
heroku login

# Create app if it doesn't exist
if ! heroku apps:info $HEROKU_APP_NAME &> /dev/null; then
    heroku create $HEROKU_APP_NAME
fi

# Deploy
git push heroku main

echo "✅ Deployment complete!" """
    
    def _generate_digitalocean_script(self, project_type: str) -> str:
        """Generate DigitalOcean deployment script"""
        return """#!/bin/bash
# DigitalOcean Deployment Script

echo "🚀 Deploying to DigitalOcean..."

# Build the project
npm run build

# Deploy using doctl or other methods
echo "Please deploy manually through DigitalOcean dashboard"
echo "or set up continuous deployment with GitHub Actions." """
    
    def _generate_generic_deployment_script(self, project_type: str) -> str:
        """Generate generic deployment script"""
        return """#!/bin/bash
# Generic Deployment Script

echo "🚀 Starting deployment process..."

# Build the project
echo "Building project..."
npm run build

# Run tests
echo "Running tests..."
npm test

# Deploy (customize this section)
echo "Please customize this deployment script for your specific hosting provider."

echo "✅ Deployment script ready!" """