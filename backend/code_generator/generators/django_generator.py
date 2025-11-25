import os
from typing import Dict, List, Any
from .base_generator import BaseGenerator

class DjangoGenerator(BaseGenerator):
    """Django backend generator"""
    
    def __init__(self):
        super().__init__()
        self.framework_name = "django"
        self.supported_features = [
            'authentication', 'rest_api', 'database_models', 'admin_panel',
            'user_management', 'file_upload', 'caching'
        ]
    
    def generate_project_structure(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate complete Django project structure"""
        files = {}
        
        project_name = specifications.get('project_name', 'myproject')
        app_name = specifications.get('app_name', 'core')
        
        # Django project files
        files.update(self._generate_django_settings(project_name, specifications))
        files.update(self._generate_urls_files(project_name))
        files.update(self._generate_requirements(specifications))
        
        # Django app files
        files.update(self._generate_app_files(app_name, specifications))
        
        # Management files
        files.update(self._generate_management_files(project_name))
        
        return files
    
    def generate_main_files(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate main Django application files"""
        return {}
    
    def _generate_django_settings(self, project_name: str, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate Django settings files"""
        settings_files = {}
        
        # settings.py
        database_config = self._get_database_config(specifications)
        installed_apps = self._get_installed_apps(specifications)
        
        settings_files[f'{project_name}/settings.py'] = f"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    {installed_apps}
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{project_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

{database_config}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""
        
        # __init__.py files
        settings_files[f'{project_name}/__init__.py'] = ''
        settings_files[f'{project_name}/wsgi.py'] = f"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
application = get_wsgi_application()
"""
        
        settings_files[f'{project_name}/asgi.py'] = f"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
application = get_asgi_application()
"""
        
        return settings_files
    
    def _generate_urls_files(self, project_name: str) -> Dict[str, str]:
        """Generate URL configuration files"""
        return {
            f'{project_name}/urls.py': f"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]
""",
            'core/urls.py': """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
]
"""
        }
    
    def _generate_app_files(self, app_name: str, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate Django app files"""
        app_files = {}
        
        # Models
        app_files[f'{app_name}/models.py'] = self._generate_models(specifications)
        
        # Views
        app_files[f'{app_name}/views.py'] = self._generate_views(specifications)
        
        # Admin
        app_files[f'{app_name}/admin.py'] = self._generate_admin(specifications)
        
        # App config
        app_files[f'{app_name}/apps.py'] = f"""
from django.apps import AppConfig

class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app_name}'
"""
        
        # __init__.py files
        app_files[f'{app_name}/__init__.py'] = ''
        app_files[f'{app_name}/migrations/__init__.py'] = ''
        
        return app_files
    
    def _generate_models(self, specifications: Dict[str, Any]) -> str:
        """Generate Django models"""
        models_code = """from django.db import models
from django.contrib.auth.models import AbstractUser

"""
        features = specifications.get('features', [])
        
        if 'user_management' in features:
            models_code += """
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

"""
        
        if 'blog' in features:
            models_code += """
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

"""
        
        return models_code
    
    def _generate_views(self, specifications: Dict[str, Any]) -> str:
        """Generate Django views"""
        return """from django.http import JsonResponse
from django.shortcuts import render

def api_root(request):
    return JsonResponse({
        'message': 'Welcome to Django API',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/'
        }
    })

def home(request):
    return render(request, 'home.html')
"""
    
    def _generate_admin(self, specifications: Dict[str, Any]) -> str:
        """Generate Django admin configuration"""
        admin_code = """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
"""
        
        features = specifications.get('features', [])
        
        if 'user_management' in features:
            admin_code += """
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'created_at')
"""
        
        if 'blog' in features:
            admin_code += """
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')
"""
        
        return admin_code
    
    def _generate_requirements(self, specifications: Dict[str, Any]) -> Dict[str, str]:
        """Generate requirements.txt"""
        requirements = ["Django>=4.2.0"]
        
        features = specifications.get('features', [])
        if 'rest_api' in features:
            requirements.append("djangorestframework>=3.14.0")
        
        if 'database' in specifications and specifications['database'] == 'postgresql':
            requirements.append("psycopg2-binary>=2.9.0")
        
        return {
            'requirements.txt': '\n'.join(requirements)
        }
    
    def _generate_management_files(self, project_name: str) -> Dict[str, str]:
        """Generate management files"""
        return {
            'manage.py': f"""#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)
""",
            '.env.example': """DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
"""
        }
    
    def _get_database_config(self, specifications: Dict[str, Any]) -> str:
        """Get database configuration based on specifications"""
        db_type = specifications.get('database', 'sqlite')
        
        if db_type == 'postgresql':
            return """
# PostgreSQL Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""
        else:
            return """
# SQLite Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
    
    def _get_installed_apps(self, specifications: Dict[str, Any]) -> str:
        """Get installed apps configuration"""
        apps = ["'rest_framework',", "'core',"]
        
        features = specifications.get('features', [])
        if 'cors' in features:
            apps.append("'corsheaders',")
        
        return '\n    '.join(apps)