"""
Template validators for code generation
Security-focused template validation
"""

import re
import os
from typing import Dict, List, Set, Any, Tuple
from pathlib import Path

# Required template variables for different template types
REQUIRED_TEMPLATE_VARIABLES = {
    'react/app.js.tpl': {'project_name'},
    'react/index.html.tpl': {'project_name'},
    'react/packages.json.tpl': {'project_name'},
    'django/settings.py.tpl': {'project_name', 'secret_key'},
    'django/urls.py.tpl': {'project_name'},
}

# Valid variable name pattern
VALID_VARIABLE_PATTERN = r'^[a-zA-Z_][a-zA-Z0-9_]*$'

# Security-sensitive template patterns
SECURITY_SENSITIVE_PATTERNS = {
    'secret_key': r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]{20,}$',
    'password': r'^.{8,}$',
    'api_key': r'^[a-zA-Z0-9]{20,}$'
}

def validate_template_variables(template_content: str, required_variables: Set[str], provided_variables: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate template variables
    
    Args:
        template_content: Content of the template
        required_variables: Set of required variable names
        provided_variables: Dictionary of provided variables
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Extract variables from template (looking for {{ variable_name }} pattern)
    template_vars = set(re.findall(r'{{\s*([a-zA-Z0-9_]+)\s*}}', template_content))
    
    # Check for required variables
    missing_vars = required_variables - template_vars
    if missing_vars:
        errors.append(f"Missing required variables in template: {', '.join(missing_vars)}")
    
    # Check if all required variables are provided
    missing_provided = required_variables - set(provided_variables.keys())
    if missing_provided:
        errors.append(f"Missing required variable values: {', '.join(missing_provided)}")
    
    # Validate variable names in template
    for var_name in template_vars:
        if not re.match(VALID_VARIABLE_PATTERN, var_name):
            errors.append(f"Invalid variable name in template: '{var_name}'")
    
    # Check for unused provided variables
    unused_vars = set(provided_variables.keys()) - template_vars
    if unused_vars:
        errors.append(f"Unused provided variables: {', '.join(unused_vars)}")
    
    # Security validation for sensitive variables
    for var_name, value in provided_variables.items():
        if var_name in SECURITY_SENSITIVE_PATTERNS:
            pattern = SECURITY_SENSITIVE_PATTERNS[var_name]
            if not re.match(pattern, str(value)):
                errors.append(f"Weak {var_name} detected. Ensure it meets security requirements.")
    
    return len(errors) == 0, errors

def validate_template_file(template_path: str, provided_variables: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a template file and its variables
    
    Args:
        template_path: Path to the template file
        provided_variables: Variables provided for template rendering
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check if template file exists
    if not os.path.exists(template_path):
        return False, [f"Template file does not exist: {template_path}"]
    
    # Read template content
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except Exception as e:
        return False, [f"Error reading template file: {str(e)}"]
    
    # Get required variables for this template
    template_key = str(Path(template_path).relative_to(Path(template_path).parent.parent.parent))
    required_vars = REQUIRED_TEMPLATE_VARIABLES.get(template_key, set())
    
    # Validate variables
    is_valid, var_errors = validate_template_variables(template_content, required_vars, provided_variables)
    errors.extend(var_errors)
    
    # Additional template-specific validations
    if template_path.endswith('.json.tpl'):
        # Basic JSON template validation
        if '{{' in template_content and '}}' in template_content:
            # Check if JSON structure is maintained around variables
            lines = template_content.split('\n')
            for i, line in enumerate(lines, 1):
                if '{{' in line and '}}' in line:
                    # Check if variable is properly placed in JSON
                    if not ('"' in line or "'" in line):
                        errors.append(f"Template variable not in string context at line {i}")
    
    # Security validation for specific template types
    if 'settings.py.tpl' in template_path:
        security_errors = validate_django_settings_template(template_content)
        errors.extend(security_errors)
    
    elif 'urls.py.tpl' in template_path:
        security_errors = validate_urls_template(template_content)
        errors.extend(security_errors)
    
    return len(errors) == 0, errors

def validate_django_settings_template(content: str) -> List[str]:
    """
    Validate Django settings template for security issues
    
    Args:
        content: Template content
        
    Returns:
        List of security issues
    """
    issues = []
    
    # Check for insecure default settings
    insecure_patterns = [
        (r'DEBUG\s*=\s*True', 'DEBUG should be False in production'),
        (r'ALLOWED_HOSTS\s*=\s*\[\]', 'ALLOWED_HOSTS should not be empty'),
        (r'SECRET_KEY\s*=\s*[\'\"][^\'\"]{0,20}[\'\"]', 'SECRET_KEY is too short'),
    ]
    
    for pattern, message in insecure_patterns:
        if re.search(pattern, content):
            issues.append(f"Security issue in settings template: {message}")
    
    # Check for missing security settings
    required_settings = [
        'SECURE_HSTS_SECONDS',
        'SECURE_CONTENT_TYPE_NOSNIFF',
        'SECURE_BROWSER_XSS_FILTER',
        'SESSION_COOKIE_SECURE',
        'CSRF_COOKIE_SECURE'
    ]
    
    for setting in required_settings:
        if setting not in content:
            issues.append(f"Missing security setting in template: {setting}")
    
    return issues

def validate_urls_template(content: str) -> List[str]:
    """
    Validate URLs template for security issues
    
    Args:
        content: Template content
        
    Returns:
        List of security issues
    """
    issues = []
    
    # Check for insecure URL patterns
    insecure_patterns = [
        (r'path\s*\(\s*[\'\"][^\'\"]*\.\.[^\'\"]*[\'\"]', 'Potential path traversal in URL pattern'),
    ]
    
    for pattern, message in insecure_patterns:
        if re.search(pattern, content):
            issues.append(f"Security issue in URLs template: {message}")
    
    return issues

def validate_template_directory(template_dir: str, context: Dict[str, Any]) -> Tuple[bool, Dict[str, List[str]]]:
    """
    Validate all templates in a directory
    
    Args:
        template_dir: Directory containing templates
        context: Template context variables
        
    Returns:
        Tuple of (is_valid, dict_of_errors_by_file)
    """
    errors_by_file = {}
    all_valid = True
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.tpl'):
                template_path = os.path.join(root, file)
                is_valid, errors = validate_template_file(template_path, context)
                if not is_valid:
                    errors_by_file[template_path] = errors
                    all_valid = False
    
    return all_valid, errors_by_file

def generate_template_security_report(template_dir: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive security report for templates
    
    Args:
        template_dir: Directory containing templates
        context: Template context variables
        
    Returns:
        Security report
    """
    report = {
        'total_templates': 0,
        'valid_templates': 0,
        'invalid_templates': 0,
        'security_issues': [],
        'recommendations': []
    }
    
    is_valid, errors_by_file = validate_template_directory(template_dir, context)
    
    report['total_templates'] = len(errors_by_file)
    report['valid_templates'] = sum(1 for errors in errors_by_file.values() if len(errors) == 0)
    report['invalid_templates'] = report['total_templates'] - report['valid_templates']
    
    # Collect all security issues
    for file_path, errors in errors_by_file.items():
        for error in errors:
            if 'security' in error.lower() or any(keyword in error.lower() for keyword in ['insecure', 'vulnerability', 'weak']):
                report['security_issues'].append({
                    'file': file_path,
                    'issue': error
                })
    
    # Generate recommendations
    if report['security_issues']:
        report['recommendations'].append("Review and fix security issues in templates before generation")
    
    if any('SECRET_KEY' in issue['issue'] for issue in report['security_issues']):
        report['recommendations'].append("Ensure SECRET_KEY is sufficiently long and random")
    
    if any('DEBUG' in issue['issue'] for issue in report['security_issues']):
        report['recommendations'].append("Set DEBUG=False for production environments")
    
    return report