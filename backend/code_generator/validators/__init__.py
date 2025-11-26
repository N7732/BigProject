"""
Security-focused validators for AI-generated code
Comprehensive cybersecurity validation suite
"""

import os
from .dependency_checker import (
    check_vulnerable_dependencies,
    validate_dependency_versions,
    scan_for_malicious_packages,
    check_license_compliance,
    comprehensive_dependency_scan,
    is_version_vulnerable
)

from .security_scanner import (
    SecurityScanner,
    scan_code_for_vulnerabilities,
    check_security_headers,
    validate_authentication_flow,
    check_data_protection,
    generate_security_recommendations
)

from .syntax_validator import (
    validate_python_syntax,
    validate_javascript_syntax,
    validate_html_security,
    validate_sql_injection_risks,
    validate_xss_vulnerabilities,
    check_python_security_patterns,
    check_javascript_security_patterns,
    comprehensive_syntax_validation
)

from .model_varidator import (
    validate_model_name,
    validate_field_name,
    validate_field_type,
    validate_field_parameters,
    validate_field_definition,
    validate_model_fields
)

from .template_validator import (
    validate_template_variables,
    validate_template_file,
    validate_template_directory
)

from .project_validator import (
    validate_project_name,
    validate_app_name,
    validate_directory_path,
    validate_secret_key,
    validate_database_config
)

# Main validation function
def validate_complete_project(project_path: str, context: dict) -> dict:
    """
    Comprehensive validation of a generated project
    
    Args:
        project_path: Path to the generated project
        context: Project context and variables
        
    Returns:
        Complete validation report
    """
    report = {
        'project_info': {
            'path': project_path,
            'context': context
        },
        'security_scan': {},
        'syntax_validation': {},
        'dependency_check': {},
        'model_validation': {},
        'template_validation': {},
        'project_validation': {},
        'summary': {
            'passed': False,
            'total_issues': 0,
            'critical_issues': 0,
            'security_score': 0
        }
    }
    
    try:
        # Security scanning
        report['security_scan'] = scan_code_for_vulnerabilities(project_path)
        
        # Dependency checking (if package files exist)
        import os
        requirements_path = os.path.join(project_path, 'requirements.txt')
        if os.path.exists(requirements_path):
            # Parse dependencies and check
            dependencies = parse_requirements_file(requirements_path)
            report['dependency_check'] = comprehensive_dependency_scan(dependencies)
        
        # Syntax validation for key files
        report['syntax_validation'] = validate_key_files_syntax(project_path)
        
        # Template validation
        report['template_validation'] = validate_template_directory(
            os.path.join(project_path, 'templates'), 
            context
        )
        
        # Project-level validation
        report['project_validation'] = validate_project_structure(project_path, context)
        
        # Calculate summary
        report['summary'] = calculate_validation_summary(report)
        
    except Exception as e:
        report['error'] = f"Validation failed: {str(e)}"
    
    return report

def parse_requirements_file(requirements_path: str) -> dict:
    """Parse requirements.txt file into dependency dict"""
    dependencies = {}
    try:
        with open(requirements_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '==' in line:
                    pkg, version = line.split('==', 1)
                    dependencies[pkg.strip()] = version.strip()
    except Exception:
        pass
    return dependencies

def validate_key_files_syntax(project_path: str) -> dict:
    """Validate syntax of key project files"""
    results = {}
    key_files = [
        'manage.py',
        'settings.py',
        'urls.py',
        'wsgi.py'
    ]
    
    for file_name in key_files:
        file_path = os.path.join(project_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            results[file_name] = comprehensive_syntax_validation(file_path, content)
    
    return results

def validate_project_structure(project_path: str, context: dict) -> dict:
    """Validate overall project structure"""
    issues = []
    
    required_dirs = ['static', 'templates', 'media']
    required_files = ['manage.py', 'requirements.txt']
    
    for dir_name in required_dirs:
        dir_path = os.path.join(project_path, dir_name)
        if not os.path.exists(dir_path):
            issues.append(f"Missing directory: {dir_name}")
    
    for file_name in required_files:
        file_path = os.path.join(project_path, file_name)
        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file_name}")
    
    # Validate project name
    is_valid, error = validate_project_name(context.get('project_name', ''))
    if not is_valid:
        issues.append(f"Invalid project name: {error}")
    
    return {
        'is_valid': len(issues) == 0,
        'issues': issues
    }

def calculate_validation_summary(report: dict) -> dict:
    """Calculate overall validation summary"""
    total_issues = 0
    critical_issues = 0
    
    # Count security issues
    security_issues = report.get('security_scan', {}).get('summary', {})
    total_issues += security_issues.get('total_issues', 0)
    critical_issues += security_issues.get('critical', 0)
    
    # Count dependency issues
    dep_summary = report.get('dependency_check', {}).get('summary', {})
    total_issues += dep_summary.get('vulnerable_packages', 0)
    total_issues += dep_summary.get('suspicious_packages', 0)
    
    # Count syntax issues
    for file_result in report.get('syntax_validation', {}).values():
        total_issues += file_result.get('summary', {}).get('total_issues', 0)
        critical_issues += file_result.get('summary', {}).get('critical', 0)
    
    # Calculate security score (0-100)
    security_score = max(0, 100 - (total_issues * 5) - (critical_issues * 20))
    
    return {
        'passed': critical_issues == 0 and total_issues < 10,
        'total_issues': total_issues,
        'critical_issues': critical_issues,
        'security_score': min(100, security_score),
        'recommendations': report.get('security_scan', {}).get('recommendations', [])
    }

__all__ = [
    # Dependency Checker
    'check_vulnerable_dependencies',
    'validate_dependency_versions',
    'scan_for_malicious_packages',
    'check_license_compliance',
    'comprehensive_dependency_scan',
    'is_version_vulnerable',
    
    # Security Scanner
    'SecurityScanner',
    'scan_code_for_vulnerabilities',
    'check_security_headers',
    'validate_authentication_flow',
    'check_data_protection',
    'generate_security_recommendations',
    
    # Syntax Validator
    'validate_python_syntax',
    'validate_javascript_syntax',
    'validate_html_security',
    'validate_sql_injection_risks',
    'validate_xss_vulnerabilities',
    'check_python_security_patterns',
    'check_javascript_security_patterns',
    'comprehensive_syntax_validation',
    
    # Model Validators
    'validate_model_name',
    'validate_field_name',
    'validate_field_type',
    'validate_field_parameters',
    'validate_field_definition',
    'validate_model_fields',
    
    # Template Validators
    'validate_template_variables',
    'validate_template_file',
    'validate_template_directory',
    
    # Project Validators
    'validate_project_name',
    'validate_app_name',
    'validate_directory_path',
    'validate_secret_key',
    'validate_database_config',
    
    # Main validation function
    'validate_complete_project'
]