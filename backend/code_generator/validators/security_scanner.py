"""
Security scanner for AI-generated code with cybersecurity focus
Comprehensive security analysis for generated codebases
"""

import re
import ast
import secrets
from typing import List, Dict, Set, Tuple, Any
from pathlib import Path

class SecurityScanner:
    """
    Comprehensive security scanner for generated code
    """
    
    def __init__(self):
        self.security_issues = []
        self.critical_patterns = self._load_critical_patterns()
    
    def _load_critical_patterns(self) -> Dict[str, List[str]]:
        """Load security-critical patterns to scan for"""
        return {
            'hardcoded_secrets': [
                r'password\s*=\s*[\'"][^\'"]+[\'"]',
                r'secret_key\s*=\s*[\'"][^\'"]+[\'"]',
                r'api_key\s*=\s*[\'"][^\'"]+[\'"]',
                r'token\s*=\s*[\'"][^\'"]+[\'"]',
                r'aws_secret\s*=\s*[\'"][^\'"]+[\'"]',
                r'database_password\s*=\s*[\'"][^\'"]+[\'"]',
                r'private_key\s*=\s*[\'"][^\'"]+[\'"]',
                r'client_secret\s*=\s*[\'"][^\'"]+[\'"]',
            ],
            'insecure_directives': [
                r'DEBUG\s*=\s*True',
                r'ALLOWED_HOSTS\s*=\s*\[\s*[\'"]\*[\'"]\s*\]',
                r'CORS_ORIGIN_ALLOW_ALL\s*=\s*True',
                r'CSRF_COOKIE_SECURE\s*=\s*False',
                r'SESSION_COOKIE_SECURE\s*=\s*False',
                r'SECURE_SSL_REDIRECT\s*=\s*False',
                r'SECURE_HSTS_SECONDS\s*=\s*0',
            ],
            'dangerous_functions': [
                r'eval\s*\(',
                r'exec\s*\(',
                r'__import__\s*\(',
                r'os\.system\s*\(',
                r'subprocess\.call\s*\(',
                r'pickle\.loads\s*\(',
                r'marshal\.loads\s*\(',
                r'compile\s*\(',
            ],
            'sql_injection_risks': [
                r'cursor\.execute\s*\(\s*f"[^"]*"',
                r'cursor\.execute\s*\(\s*"[^"]*"\s*%\s*',
                r'raw\s*\(\s*"[^"]*"\s*\)',
                r'extra\s*\(\s*where\s*=',
                r'\.filter\s*\(\s*[^)]*F\s*\(',
            ],
            'xss_patterns': [
                r'\.innerHTML\s*=',
                r'\.outerHTML\s*=',
                r'document\.write\s*\(',
                r'\.html\s*\(\s*[^)]+\)',
                r'React\.createElement\s*\(\s*[^,]+,\s*\{[^}]*dangerouslySetInnerHTML',
                r'\{.*\}\s*\)\s*\)',  # JSX without proper escaping
            ],
            'insecure_authentication': [
                r'password\s*=\s*[\'"]\w+[\'"]',  # Simple passwords
                r'SECRET_KEY\s*=\s*[\'"]\w{1,20}[\'"]',  # Short secret keys
                r'algorithm\s*=\s*[\'"]HS256[\'"]',  # Weak JWT algorithm
            ]
        }
    
    def scan_file(self, file_path: str, content: str) -> List[Dict]:
        """
        Scan a single file for security issues
        
        Args:
            file_path: Path to the file
            content: File content
            
        Returns:
            List of security issues found
        """
        file_issues = []
        file_ext = Path(file_path).suffix.lower()
        
        # Python-specific scans
        if file_ext == '.py':
            file_issues.extend(self._scan_python_file(content, file_path))
        
        # JavaScript/JSX-specific scans
        elif file_ext in ['.js', '.jsx']:
            file_issues.extend(self._scan_javascript_file(content, file_path))
        
        # HTML-specific scans
        elif file_ext == '.html':
            file_issues.extend(self._scan_html_file(content, file_path))
        
        # Django template scans
        elif file_ext in ['.html', '.htm'] and 'templates' in file_path:
            file_issues.extend(self._scan_django_template(content, file_path))
        
        # General pattern matching for all files
        file_issues.extend(self._pattern_scan(content, file_path))
        
        return file_issues
    
    def _scan_python_file(self, content: str, file_path: str) -> List[Dict]:
        """Scan Python file for security issues"""
        issues = []
        
        try:
            tree = ast.parse(content)
            
            # AST-based security checks
            for node in ast.walk(tree):
                # Check for unsafe deserialization
                if isinstance(node, ast.Call):
                    if (isinstance(node.func, ast.Attribute) and 
                        isinstance(node.func.value, ast.Name) and
                        node.func.value.id == 'pickle' and
                        node.func.attr == 'loads'):
                        issues.append({
                            'file': file_path,
                            'line': node.lineno,
                            'severity': 'HIGH',
                            'category': 'unsafe_deserialization',
                            'message': 'Unsafe pickle deserialization detected. Use json or other safe serialization methods.',
                            'code': ast.get_source_segment(content, node)
                        })
                
                # Check for shell command execution
                if (isinstance(node, ast.Call) and
                    isinstance(node.func, ast.Attribute) and
                    node.func.attr in ['system', 'popen', 'call', 'run'] and
                    isinstance(node.func.value, ast.Name) and
                    node.func.value.id == 'os'):
                    issues.append({
                        'file': file_path,
                        'line': node.lineno,
                        'severity': 'MEDIUM',
                        'category': 'command_injection',
                        'message': 'Potential command injection risk. Use subprocess with proper argument handling.',
                        'code': ast.get_source_segment(content, node)
                    })
                
                # Check for weak cryptography
                if (isinstance(node, ast.Call) and
                    isinstance(node.func, ast.Name) and
                    node.func.id == 'md5'):
                    issues.append({
                        'file': file_path,
                        'line': node.lineno,
                        'severity': 'HIGH',
                        'category': 'weak_cryptography',
                        'message': 'MD5 is cryptographically broken. Use SHA-256 or bcrypt.',
                        'code': ast.get_source_segment(content, node)
                    })
                
                # Check for potential path traversal
                if (isinstance(node, ast.Call) and
                    isinstance(node.func, ast.Attribute) and
                    node.func.attr == 'open' and
                    isinstance(node.func.value, ast.Name) and
                    node.func.value.id == 'os'):
                    issues.append({
                        'file': file_path,
                        'line': node.lineno,
                        'severity': 'MEDIUM',
                        'category': 'path_traversal',
                        'message': 'Potential path traversal vulnerability. Validate user input for file operations.',
                        'code': ast.get_source_segment(content, node)
                    })
        
        except SyntaxError as e:
            issues.append({
                'file': file_path,
                'line': e.lineno,
                'severity': 'MEDIUM',
                'category': 'syntax_error',
                'message': f'Syntax error in Python file: {str(e)}',
                'code': ''
            })
        
        return issues
    
    def _scan_javascript_file(self, content: str, file_path: str) -> List[Dict]:
        """Scan JavaScript file for security issues"""
        issues = []
        
        # Check for eval usage
        eval_pattern = r'eval\s*\([^)]\)'
        for match in re.finditer(eval_pattern, content):
            issues.append({
                'file': file_path,
                'line': self._get_line_number(content, match.start()),
                'severity': 'HIGH',
                'category': 'code_injection',
                'message': 'eval() function detected. This can lead to code injection vulnerabilities.',
                'code': match.group()
            })
        
        # Check for innerHTML usage without sanitization
        inner_html_pattern = r'\.innerHTML\s*='
        for match in re.finditer(inner_html_pattern, content):
            issues.append({
                'file': file_path,
                'line': self._get_line_number(content, match.start()),
                'severity': 'MEDIUM',
                'category': 'xss',
                'message': 'innerHTML assignment detected. Ensure proper XSS protection.',
                'code': match.group()
            })
        
        # Check for localStorage with sensitive data
        localStorage_pattern = r'localStorage\.setItem\s*\(\s*[\'"][^\'"]*(password|token|secret)[^\'"]*[\'"]'
        for match in re.finditer(localStorage_pattern, content, re.IGNORECASE):
            issues.append({
                'file': file_path,
                'line': self._get_line_number(content, match.start()),
                'severity': 'MEDIUM',
                'category': 'data_exposure',
                'message': 'Sensitive data stored in localStorage. Consider more secure storage.',
                'code': match.group()
            })
        
        # Check for inline event handlers
        inline_event_pattern = r'on\w+\s*=\s*[\'\"][^\'\"]*[\'\"]'
        for match in re.finditer(inline_event_pattern, content):
            issues.append({
                'file': file_path,
                'line': self._get_line_number(content, match.start()),
                'severity': 'LOW',
                'category': 'xss',
                'message': 'Inline event handler detected. Consider separating behavior from content.',
                'code': match.group()
            })
        
        return issues
    
    def _scan_html_file(self, content: str, file_path: str) -> List[Dict]:
        """Scan HTML file for security issues"""
        issues = []
        
        # Check for missing CSRF protection
        if '<form' in content and 'csrf' not in content.lower():
            issues.append({
                'file': file_path,
                'line': 1,
                'severity': 'MEDIUM',
                'category': 'csrf',
                'message': 'Form detected without obvious CSRF protection.',
                'code': 'Form elements found'
            })
        
        # Check for inline scripts without nonce/CSP
        script_pattern = r'<script(?![^>]*nonce)(?![^>]*src)[^>]*>'
        for match in re.finditer(script_pattern, content, re.IGNORECASE):
            issues.append({
                'file': file_path,
                'line': self._get_line_number(content, match.start()),
                'severity': 'LOW',
                'category': 'xss',
                'message': 'Inline script without nonce attribute. Consider using Content Security Policy.',
                'code': match.group()
            })
        
        # Check for target="_blank" without rel="noopener"
        target_blank_pattern = r'target\s*=\s*[\'"]_blank[\'"]'
        rel_pattern = r'rel\s*=\s*[\'"]\w*noopener\w*[\'"]'
        
        for match in re.finditer(target_blank_pattern, content, re.IGNORECASE):
            if not re.search(rel_pattern, content[match.start():match.start()+200]):
                issues.append({
                    'file': file_path,
                    'line': self._get_line_number(content, match.start()),
                    'severity': 'LOW',
                    'category': 'security_misconfiguration',
                    'message': 'target="_blank" without rel="noopener" can be a security risk.',
                    'code': match.group()
                })
        
        return issues
    
    def _scan_django_template(self, content: str, file_path: str) -> List[Dict]:
        """Scan Django templates for security issues"""
        issues = []
        
        # Check for autoescape off
        if '{% autoescape off %}' in content:
            issues.append({
                'file': file_path,
                'line': content.find('{% autoescape off %}') + 1,
                'severity': 'HIGH',
                'category': 'xss',
                'message': 'Autoescape turned off in template. This can lead to XSS vulnerabilities.',
                'code': '{% autoescape off %}'
            })
        
        # Check for unsafe filter usage
        unsafe_filters = ['safe', 'escapejs']
        for filter_name in unsafe_filters:
            filter_pattern = f'\\|{filter_name}'
            for match in re.finditer(filter_pattern, content):
                issues.append({
                    'file': file_path,
                    'line': self._get_line_number(content, match.start()),
                    'severity': 'MEDIUM',
                    'category': 'xss',
                    'message': f'Unsafe filter |{filter_name} detected. Ensure proper input validation.',
                    'code': match.group()
                })
        
        return issues
    
    def _pattern_scan(self, content: str, file_path: str) -> List[Dict]:
        """General pattern-based security scanning"""
        issues = []
        
        for category, patterns in self.critical_patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    severity = self._get_severity_for_category(category)
                    issues.append({
                        'file': file_path,
                        'line': self._get_line_number(content, match.start()),
                        'severity': severity,
                        'category': category,
                        'message': self._get_message_for_category(category),
                        'code': match.group()
                    })
        
        return issues
    
    def _get_severity_for_category(self, category: str) -> str:
        """Get severity level for security category"""
        severity_map = {
            'hardcoded_secrets': 'CRITICAL',
            'dangerous_functions': 'HIGH',
            'sql_injection_risks': 'HIGH',
            'insecure_authentication': 'HIGH',
            'insecure_directives': 'MEDIUM',
            'xss_patterns': 'MEDIUM'
        }
        return severity_map.get(category, 'LOW')
    
    def _get_message_for_category(self, category: str) -> str:
        """Get descriptive message for security category"""
        message_map = {
            'hardcoded_secrets': 'Hardcoded secret detected. Use environment variables or secure secret management.',
            'insecure_directives': 'Insecure configuration directive detected.',
            'dangerous_functions': 'Potentially dangerous function call detected.',
            'sql_injection_risks': 'Potential SQL injection vulnerability.',
            'xss_patterns': 'Potential Cross-Site Scripting (XSS) vulnerability.',
            'insecure_authentication': 'Insecure authentication configuration detected.'
        }
        return message_map.get(category, 'Security issue detected.')
    
    def _get_line_number(self, content: str, position: int) -> int:
        """Get line number from character position"""
        return content[:position].count('\n') + 1

def scan_code_for_vulnerabilities(codebase_path: str) -> Dict[str, any]:
    """
    Comprehensive security scan of generated codebase
    
    Args:
        codebase_path: Path to the generated codebase
        
    Returns:
        Security scan results
    """
    scanner = SecurityScanner()
    all_issues = []
    scanned_files = 0
    
    for file_path in Path(codebase_path).rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.py', '.js', '.jsx', '.html', '.htm', '.json']:
            try:
                content = file_path.read_text(encoding='utf-8')
                issues = scanner.scan_file(str(file_path), content)
                all_issues.extend(issues)
                scanned_files += 1
            except Exception as e:
                all_issues.append({
                    'file': str(file_path),
                    'line': 0,
                    'severity': 'LOW',
                    'category': 'scan_error',
                    'message': f'Error scanning file: {str(e)}',
                    'code': ''
                })
    
    # Categorize issues
    critical_issues = [issue for issue in all_issues if issue['severity'] == 'CRITICAL']
    high_issues = [issue for issue in all_issues if issue['severity'] == 'HIGH']
    medium_issues = [issue for issue in all_issues if issue['severity'] == 'MEDIUM']
    low_issues = [issue for issue in all_issues if issue['severity'] == 'LOW']
    
    # Calculate security score
    security_score = calculate_security_score(len(all_issues), len(critical_issues), len(high_issues))
    
    return {
        'summary': {
            'scanned_files': scanned_files,
            'total_issues': len(all_issues),
            'critical': len(critical_issues),
            'high': len(high_issues),
            'medium': len(medium_issues),
            'low': len(low_issues),
            'security_score': security_score
        },
        'issues': all_issues,
        'critical_issues': critical_issues,
        'high_issues': high_issues,
        'recommendations': generate_security_recommendations(all_issues)
    }

def calculate_security_score(total_issues: int, critical: int, high: int) -> int:
    """Calculate security score (0-100) based on issues found"""
    base_score = 100
    
    # Heavy penalties for critical and high issues
    score = base_score - (critical * 30) - (high * 15) - (total_issues * 2)
    
    return max(0, min(100, score))

def check_security_headers(settings_content: str) -> List[Dict]:
    """
    Check Django settings for security headers configuration
    
    Args:
        settings_content: Django settings.py content
        
    Returns:
        List of security header issues
    """
    issues = []
    
    required_headers = {
        'SECURE_HSTS_SECONDS': 'Strict-Transport-Security',
        'SECURE_CONTENT_TYPE_NOSNIFF': 'X-Content-Type-Options',
        'SECURE_BROWSER_XSS_FILTER': 'X-XSS-Protection',
        'SECURE_SSL_REDIRECT': 'SSL redirect',
        'SESSION_COOKIE_SECURE': 'Secure session cookies',
        'CSRF_COOKIE_SECURE': 'Secure CSRF cookies',
        'X_FRAME_OPTIONS': 'Clickjacking protection'
    }
    
    for setting, description in required_headers.items():
        if setting not in settings_content:
            issues.append({
                'setting': setting,
                'description': description,
                'severity': 'MEDIUM',
                'message': f'Missing security setting: {setting}'
            })
        else:
            # Check if setting is properly configured
            if setting in ['SESSION_COOKIE_SECURE', 'CSRF_COOKIE_SECURE', 'SECURE_SSL_REDIRECT']:
                if f'{setting} = False' in settings_content:
                    issues.append({
                        'setting': setting,
                        'description': description,
                        'severity': 'HIGH',
                        'message': f'Insecure configuration: {setting} is set to False'
                    })
            
            if setting == 'X_FRAME_OPTIONS' and 'DENY' not in settings_content:
                issues.append({
                    'setting': setting,
                    'description': description,
                    'severity': 'MEDIUM',
                    'message': f'Consider setting {setting} to "DENY" for better security'
                })
    
    return issues

def validate_authentication_flow(codebase_path: str) -> List[Dict]:
    """
    Validate authentication and authorization implementation
    
    Args:
        codebase_path: Path to codebase
        
    Returns:
        List of authentication issues
    """
    issues = []
    
    # Check for common authentication issues
    auth_patterns = [
        (r'@login_required', 'Django login_required decorator', 'LOW'),
        (r'@permission_required', 'Django permission_required decorator', 'LOW'),
        (r'PasswordHasher', 'Password hasher configuration', 'MEDIUM'),
        (r'AUTH_PASSWORD_VALIDATORS', 'Password validation', 'MEDIUM'),
    ]
    
    for pattern, description, severity in auth_patterns:
        for file_path in Path(codebase_path).rglob('*.py'):
            try:
                content = file_path.read_text(encoding='utf-8')
                if re.search(pattern, content):
                    # Found the pattern, check if it's properly configured
                    if pattern == 'AUTH_PASSWORD_VALIDATORS':
                        if '[]' in content or 'AUTH_PASSWORD_VALIDATORS = []' in content:
                            issues.append({
                                'file': str(file_path),
                                'severity': 'HIGH',
                                'category': 'authentication',
                                'message': 'No password validators configured'
                            })
            except Exception:
                continue
    
    return issues

def check_data_protection(codebase_path: str) -> List[Dict]:
    """
    Check for data protection and privacy issues
    
    Args:
        codebase_path: Path to codebase
        
    Returns:
        List of data protection issues
    """
    issues = []
    
    sensitive_data_patterns = [
        r'email[^=]*=',
        r'phone[^=]*=',
        r'address[^=]*=',
        r'ssn[^=]*=',
        r'credit_card[^=]*=',
        r'password[^=]*=',
        r'personal_data[^=]*=',
        r'private_key[^=]*=',
    ]
    
    for pattern in sensitive_data_patterns:
        for file_path in Path(codebase_path).rglob('*.py'):
            try:
                content = file_path.read_text(encoding='utf-8')
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    # Check if it's in a model or form without proper protection
                    if 'models.py' in str(file_path) or 'forms.py' in str(file_path):
                        # Look for encryption or hashing in the same file
                        if not any(secure_pattern in content for secure_pattern in ['bcrypt', 'PBKDF2', 'encrypt', 'hash']):
                            issues.append({
                                'file': str(file_path),
                                'line': content[:match.start()].count('\n') + 1,
                                'severity': 'MEDIUM',
                                'category': 'data_protection',
                                'message': f'Sensitive data field detected without obvious protection: {match.group()}',
                                'code': match.group()
                            })
            except Exception:
                continue
    
    return issues

def generate_security_recommendations(issues: List[Dict]) -> List[str]:
    """
    Generate security recommendations based on found issues
    
    Args:
        issues: List of security issues
        
    Returns:
        List of recommendations
    """
    recommendations = []
    
    critical_count = len([i for i in issues if i['severity'] == 'CRITICAL'])
    high_count = len([i for i in issues if i['severity'] == 'HIGH'])
    
    if critical_count > 0:
        recommendations.append("🚨 CRITICAL: Address hardcoded secrets and critical vulnerabilities immediately")
    
    if high_count > 0:
        recommendations.append("⚠️ HIGH: Fix SQL injection and code execution vulnerabilities before deployment")
    
    # Specific recommendations based on issue types
    issue_categories = set(issue['category'] for issue in issues)
    
    if 'hardcoded_secrets' in issue_categories:
        recommendations.append("🔐 Use environment variables or secret management for all credentials")
    
    if 'sql_injection_risks' in issue_categories:
        recommendations.append("🗃️ Use parameterized queries or ORM methods to prevent SQL injection")
    
    if 'xss_patterns' in issue_categories:
        recommendations.append("🛡️ Implement proper input sanitization and output encoding for XSS protection")
    
    if any('insecure_directives' in issue['category'] for issue in issues):
        recommendations.append("⚙️ Configure secure settings for production deployment")
    
    if any('insecure_authentication' in issue['category'] for issue in issues):
        recommendations.append("🔑 Implement strong authentication and password policies")
    
    # General security recommendations
    recommendations.extend([
        "🔍 Conduct regular security audits and penetration testing",
        "📚 Keep all dependencies updated with security patches",
        "👥 Implement proper access controls and principle of least privilege",
        "📝 Maintain security documentation and incident response plan"
    ])
    
    return recommendations