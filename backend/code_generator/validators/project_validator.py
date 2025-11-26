"""
Project-level validators for code generation
Cybersecurity-focused project validation
"""

import re
import keyword
import os
from typing import Tuple
from pathlib import Path

def validate_project_name(name: str) -> Tuple[bool, str]:
    """
    Validate Django project name
    
    Args:
        name: Project name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Project name cannot be empty"
    
    # Check for valid Python identifier
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
        return False, "Project name must start with a letter or underscore and contain only letters, numbers, and underscores"
    
    # Check for Python keywords
    if keyword.iskeyword(name):
        return False, f"Project name '{name}' is a Python keyword"
    
    # Check for Django reserved names
    reserved_names = {
        'django', 'test', 'admin', 'api', 'static', 'media', 'templates',
        'settings', 'urls', 'models', 'views', 'forms', 'manage'
    }
    if name.lower() in reserved_names:
        return False, f"Project name '{name}' is reserved for Django"
    
    # Check length
    if len(name) < 2:
        return False, "Project name must be at least 2 characters long"
    
    if len(name) > 50:
        return False, "Project name must be 50 characters or less"
    
    # Recommended to use lowercase with underscores
    if not re.match(r'^[a-z_][a-z0-9_]*$', name):
        return False, "Project name should be lowercase with underscores (snake_case)"
    
    # Check for suspicious names
    suspicious_names = ['test', 'demo', 'example', 'temp', 'backup']
    if any(suspicious in name.lower() for suspicious in suspicious_names):
        return False, f"Project name '{name}' may indicate test or temporary code"
    
    return True, ""

def validate_app_name(name: str) -> Tuple[bool, str]:
    """
    Validate Django app name
    
    Args:
        name: App name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "App name cannot be empty"
    
    # Check for valid Python identifier
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
        return False, "App name must start with a letter or underscore and contain only letters, numbers, and underscores"
    
    # Check for Python keywords
    if keyword.iskeyword(name):
        return False, f"App name '{name}' is a Python keyword"
    
    # Check for Django reserved names
    reserved_names = {
        'admin', 'api', 'auth', 'contenttypes', 'sessions', 'messages',
        'staticfiles', 'sites', 'redirects', 'static', 'media'
    }
    if name.lower() in reserved_names:
        return False, f"App name '{name}' conflicts with Django built-in apps"
    
    # Check length
    if len(name) < 2:
        return False, "App name must be at least 2 characters long"
    
    if len(name) > 30:
        return False, "App name must be 30 characters or less"
    
    # Recommended to use lowercase with underscores
    if not re.match(r'^[a-z_][a-z0-9_]*$', name):
        return False, "App name should be lowercase with underscores (snake_case)"
    
    return True, ""

def validate_directory_path(path: str) -> Tuple[bool, str]:
    """
    Validate directory path for project generation
    
    Args:
        path: Directory path to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not path:
        return False, "Directory path cannot be empty"
    
    path_obj = Path(path)
    
    # Check if path is absolute
    if not path_obj.is_absolute():
        return False, "Directory path must be absolute"
    
    # Check if parent directory exists and is writable
    parent_dir = path_obj.parent
    if not parent_dir.exists():
        return False, f"Parent directory does not exist: {parent_dir}"
    
    if not os.access(str(parent_dir), os.W_OK):
        return False, f"No write permission for directory: {parent_dir}"
    
    # Check if target directory already exists
    if path_obj.exists():
        return False, f"Directory already exists: {path}"
    
    # Check for valid directory name characters
    try:
        path_obj.resolve()
    except Exception as e:
        return False, f"Invalid directory path: {str(e)}"
    
    # Security check: ensure path doesn't contain suspicious patterns
    suspicious_patterns = [
        r'\.\.',  # Path traversal
        r'/~',    # Home directory reference
        r'//',    # Multiple slashes
    ]
    
    path_str = str(path_obj)
    for pattern in suspicious_patterns:
        if re.search(pattern, path_str):
            return False, f"Suspicious path pattern detected: {pattern}"
    
    return True, ""

def validate_secret_key(secret_key: str) -> Tuple[bool, str]:
    """
    Validate Django secret key
    
    Args:
        secret_key: Secret key to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not secret_key:
        return False, "Secret key cannot be empty"
    
    if len(secret_key) < 50:
        return False, "Secret key must be at least 50 characters long for security"
    
    if len(secret_key) > 100:
        return False, "Secret key must be 100 characters or less"
    
    # Check for sufficient entropy (basic check)
    unique_chars = len(set(secret_key))
    if unique_chars < 20:
        return False, "Secret key has insufficient entropy"
    
    # Check for common weak patterns
    weak_patterns = [
        r'^[a-zA-Z0-9]+$',  # Only alphanumeric
        r'^django-insecure-',  # Django default pattern
        r'(.)\1{10,}',  # Repeated characters
    ]
    
    for pattern in weak_patterns:
        if re.match(pattern, secret_key):
            return False, "Secret key pattern is too predictable"
    
    return True, ""

def validate_database_config(db_config: dict) -> Tuple[bool, str]:
    """
    Validate database configuration
    
    Args:
        db_config: Database configuration dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['engine', 'name', 'user', 'password', 'host', 'port']
    
    for field in required_fields:
        if field not in db_config:
            return False, f"Missing required database field: {field}"
    
    valid_engines = {
        'django.db.backends.postgresql',
        'django.db.backends.mysql', 
        'django.db.backends.sqlite3',
        'django.db.backends.oracle'
    }
    
    if db_config['engine'] not in valid_engines:
        return False, f"Invalid database engine: {db_config['engine']}"
    
    # Port validation
    try:
        port = int(db_config['port'])
        if port < 1 or port > 65535:
            return False, "Database port must be between 1 and 65535"
    except (ValueError, TypeError):
        return False, "Database port must be a valid integer"
    
    # Security validations
    if db_config['engine'] == 'django.db.backends.sqlite3':
        # SQLite specific validations
        db_path = db_config.get('name', '')
        if ':' in db_path or '..' in db_path:
            return False, "Potential path traversal in SQLite database path"
    
    else:
        # Remote database validations
        if db_config['host'] in ['localhost', '127.0.0.1']:
            return True, "Using local database - ensure proper network security"
        
        # Check for weak passwords in remote databases
        password = db_config.get('password', '')
        if len(password) < 8:
            return False, "Database password is too short"
    
    return True, ""

def validate_project_structure(project_path: str) -> Tuple[bool, list[str]]:
    """
    Validate project structure for security best practices
    
    Args:
        project_path: Path to the project
        
    Returns:
        Tuple of (is_valid, list_of_warnings)
    """
    warnings = []
    path_obj = Path(project_path)
    
    # Check for required directories
    required_dirs = ['static', 'templates', 'media']
    for dir_name in required_dirs:
        dir_path = path_obj / dir_name
        if not dir_path.exists():
            warnings.append(f"Missing directory: {dir_name}")
    
    # Check for required files
    required_files = ['manage.py', 'requirements.txt', 'settings.py']
    for file_name in required_files:
        file_path = path_obj / file_name
        if not file_path.exists():
            warnings.append(f"Missing file: {file_name}")
    
    # Security-specific checks
    security_checks = [
        # Check for .env file (should use .env.example instead)
        ('.env', 'Found .env file - consider using .env.example for templates'),
        
        # Check for backup files
        (r'.*\.bak$', 'Backup files detected - remove before deployment'),
        
        # Check for temporary files
        (r'.*\.tmp$', 'Temporary files detected - remove before deployment'),
    ]
    
    for pattern, message in security_checks:
        for file_path in path_obj.rglob(pattern):
            warnings.append(f"{message}: {file_path.relative_to(path_obj)}")
    
    return len(warnings) == 0, warnings

def generate_project_security_report(project_path: str, project_config: dict) -> dict[str, any]:
    """
    Generate comprehensive security report for a project
    
    Args:
        project_path: Path to the project
        project_config: Project configuration
        
    Returns:
        Security report
    """
    report = {
        'project_name': project_config.get('project_name', 'unknown'),
        'is_valid': True,
        'security_score': 100,
        'issues': [],
        'warnings': [],
        'recommendations': []
    }
    
    # Validate project name
    is_valid, error = validate_project_name(project_config.get('project_name', ''))
    if not is_valid:
        report['issues'].append(f"Project name: {error}")
        report['is_valid'] = False
        report['security_score'] -= 20
    
    # Validate secret key
    is_valid, error = validate_secret_key(project_config.get('secret_key', ''))
    if not is_valid:
        report['issues'].append(f"Secret key: {error}")
        report['is_valid'] = False
        report['security_score'] -= 30
    
    # Validate database config
    db_config = project_config.get('database', {})
    is_valid, error = validate_database_config(db_config)
    if not is_valid:
        report['issues'].append(f"Database configuration: {error}")
        report['security_score'] -= 15
    
    # Validate project structure
    is_valid, warnings = validate_project_structure(project_path)
    report['warnings'].extend(warnings)
    report['security_score'] -= len(warnings) * 2
    
    # Generate recommendations
    if report['issues']:
        report['recommendations'].append("Fix critical issues before deployment")
    
    if any('secret_key' in issue.lower() for issue in report['issues']):
        report['recommendations'].append("Generate a strong, random secret key")
    
    if any('database' in issue.lower() for issue in report['issues']):
        report['recommendations'].append("Review and secure database configuration")
    
    # General security recommendations
    report['recommendations'].extend([
        "Implement proper authentication and authorization",
        "Use HTTPS in production",
        "Set up proper logging and monitoring",
        "Regularly update dependencies",
        "Conduct security testing before deployment"
    ])
    
    report['security_score'] = max(0, min(100, report['security_score']))
    
    return report