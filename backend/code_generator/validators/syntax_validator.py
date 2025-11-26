"""
Syntax and security validator for AI-generated code
Comprehensive syntax validation with security focus
"""

import ast
import re
import json
from typing import List, Dict, Tuple, Any
import subprocess
import tempfile
import os

def validate_python_syntax(code: str, filename: str = "unknown.py") -> Tuple[bool, List[Dict]]:
    """
    Validate Python syntax and security patterns
    
    Args:
        code: Python code to validate
        filename: Source filename for error reporting
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Basic syntax validation
    try:
        ast.parse(code)
    except SyntaxError as e:
        issues.append({
            'file': filename,
            'line': e.lineno,
            'column': e.offset,
            'severity': 'HIGH',
            'category': 'syntax_error',
            'message': f'Syntax error: {e.msg}',
            'code': code.split('\n')[e.lineno - 1] if e.lineno else ''
        })
        return False, issues
    
    # Security pattern checks
    security_issues = check_python_security_patterns(code, filename)
    issues.extend(security_issues)
    
    # Code quality checks
    quality_issues = check_python_code_quality(code, filename)
    issues.extend(quality_issues)
    
    return len(issues) == 0, issues

def check_python_security_patterns(code: str, filename: str) -> List[Dict]:
    """Check Python code for security anti-patterns"""
    issues = []
    
    security_patterns = [
        # Dangerous function calls
        (r'eval\s*\(', 'eval_usage', 'HIGH', 
         'eval() function detected - potential code injection vulnerability'),
        
        (r'exec\s*\(', 'exec_usage', 'HIGH',
         'exec() function detected - potential code injection vulnerability'),
        
        (r'__import__\s*\(', 'dynamic_import', 'MEDIUM',
         'Dynamic import detected - potential security risk'),
        
        # Insecure deserialization
        (r'pickle\.loads\s*\(', 'pickle_deserialization', 'HIGH',
         'Unsafe pickle deserialization - use json or other safe formats'),
        
        (r'marshal\.loads\s*\(', 'marshal_deserialization', 'HIGH',
         'Unsafe marshal deserialization - potential code execution'),
        
        # Command injection risks
        (r'os\.system\s*\(', 'os_system', 'HIGH',
         'os.system() detected - potential command injection'),
        
        (r'subprocess\.call\s*\([^,)]*shell\s*=\s*True', 'subprocess_shell', 'HIGH',
         'subprocess with shell=True detected - command injection risk'),
        
        # Weak cryptography
        (r'hashlib\.md5\s*\(', 'weak_hash_md5', 'MEDIUM',
         'MD5 hashing detected - cryptographically weak'),
        
        (r'hashlib\.sha1\s*\(', 'weak_hash_sha1', 'MEDIUM',
         'SHA1 hashing detected - cryptographically weak'),
        
        # Hardcoded secrets
        (r'password\s*=\s*[\'\"][^\'\"]+[\'\"]', 'hardcoded_password', 'CRITICAL',
         'Hardcoded password detected - use environment variables'),
        
        (r'secret_key\s*=\s*[\'\"][^\'\"]+[\'\"]', 'hardcoded_secret', 'CRITICAL',
         'Hardcoded secret key detected - use environment variables'),
        
        (r'api_key\s*=\s*[\'\"][^\'\"]+[\'\"]', 'hardcoded_api_key', 'CRITICAL',
         'Hardcoded API key detected - use environment variables'),
        
        # Potential path traversal
        (r'open\s*\(\s*[^)]*\.\./', 'path_traversal', 'MEDIUM',
         'Potential path traversal vulnerability - validate user input'),
        
        # Insecure random number generation
        (r'random\.\w+\(\)', 'insecure_random', 'LOW',
         'Insecure random module detected - use secrets module for cryptographic operations'),
    ]
    
    for pattern, category, severity, message in security_patterns:
        for match in re.finditer(pattern, code, re.IGNORECASE):
            line_num = code[:match.start()].count('\n') + 1
            issues.append({
                'file': filename,
                'line': line_num,
                'column': match.start() - code[:match.start()].rfind('\n'),
                'severity': severity,
                'category': category,
                'message': message,
                'code': match.group()
            })
    
    # AST-based security checks
    try:
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            # Check for assert statements (can be optimized out)
            if isinstance(node, ast.Assert):
                issues.append({
                    'file': filename,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'LOW',
                    'category': 'assert_usage',
                    'message': 'assert statement detected - may be optimized out in production',
                    'code': ast.get_source_segment(code, node)
                })
            
            # Check for broad except clauses
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append({
                    'file': filename,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'MEDIUM',
                    'category': 'bare_except',
                    'message': 'Bare except clause detected - may catch unexpected exceptions',
                    'code': ast.get_source_segment(code, node)
                })
            
            # Check for potential SQL injection in string formatting
            if (isinstance(node, ast.Call) and
                isinstance(node.func, ast.Attribute) and
                node.func.attr == 'execute' and
                len(node.args) > 0 and
                isinstance(node.args[0], ast.JoinedStr)):
                issues.append({
                    'file': filename,
                    'line': node.lineno,
                    'column': node.col_offset,
                    'severity': 'HIGH',
                    'category': 'sql_injection',
                    'message': 'Potential SQL injection with f-string in execute()',
                    'code': ast.get_source_segment(code, node)
                })
    
    except SyntaxError:
        # Already handled above
        pass
    
    return issues

def check_python_code_quality(code: str, filename: str) -> List[Dict]:
    """Check Python code for quality issues"""
    issues = []
    
    quality_patterns = [
        (r'print\s*\(', 'print_statement', 'LOW',
         'print() statement detected - consider using logging for production'),
        
        (r'# TODO', 'todo_comment', 'LOW',
         'TODO comment detected - address before production'),
        
        (r'# FIXME', 'fixme_comment', 'LOW',
         'FIXME comment detected - address before production'),
        
        (r'from\s+\w+\s+import\s*\*', 'wildcard_import', 'LOW',
         'Wildcard import detected - can lead to namespace pollution'),
    ]
    
    for pattern, category, severity, message in quality_patterns:
        for match in re.finditer(pattern, code):
            line_num = code[:match.start()].count('\n') + 1
            issues.append({
                'file': filename,
                'line': line_num,
                'column': match.start() - code[:match.start()].rfind('\n'),
                'severity': severity,
                'category': category,
                'message': message,
                'code': match.group()
            })
    
    return issues

def validate_javascript_syntax(code: str, filename: str = "unknown.js") -> Tuple[bool, List[Dict]]:
    """
    Validate JavaScript syntax and security patterns
    
    Args:
        code: JavaScript code to validate
        filename: Source filename for error reporting
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Security pattern checks
    security_issues = check_javascript_security_patterns(code, filename)
    issues.extend(security_issues)
    
    # Basic syntax validation using node.js (if available)
    syntax_issues = validate_js_with_node(code, filename)
    issues.extend(syntax_issues)
    
    return len(issues) == 0, issues

def check_javascript_security_patterns(code: str, filename: str) -> List[Dict]:
    """Check JavaScript code for security anti-patterns"""
    issues = []
    
    security_patterns = [
        # Dangerous function calls
        (r'eval\s*\(', 'eval_usage', 'HIGH',
         'eval() function detected - potential code injection vulnerability'),
        
        (r'setTimeout\s*\(\s*[^,)]+\)', 'setTimeout_string', 'MEDIUM',
         'setTimeout with string argument - potential code injection'),
        
        (r'setInterval\s*\(\s*[^,)]+\)', 'setInterval_string', 'MEDIUM',
         'setInterval with string argument - potential code injection'),
        
        # XSS vulnerabilities
        (r'\.innerHTML\s*=', 'innerHTML_assignment', 'MEDIUM',
         'innerHTML assignment detected - potential XSS vulnerability'),
        
        (r'\.outerHTML\s*=', 'outerHTML_assignment', 'MEDIUM',
         'outerHTML assignment detected - potential XSS vulnerability'),
        
        (r'document\.write\s*\(', 'document_write', 'MEDIUM',
         'document.write() detected - potential XSS vulnerability'),
        
        # Insecure storage
        (r'localStorage\.setItem\s*\(\s*[\'\"][^\'\"]*password[^\'\"]*[\'\"]', 
         'localStorage_password', 'MEDIUM',
         'Password storage in localStorage - consider more secure storage'),
        
        (r'sessionStorage\.setItem\s*\(\s*[\'\"][^\'\"]*token[^\'\"]*[\'\"]',
         'sessionStorage_token', 'MEDIUM',
         'Token storage in sessionStorage - consider HTTP-only cookies'),
        
        # React-specific security issues
        (r'dangerouslySetInnerHTML', 'dangerouslySetInnerHTML', 'MEDIUM',
         'dangerouslySetInnerHTML detected - ensure proper sanitization'),
        
        # Potential prototype pollution
        (r'__proto__', 'prototype_pollution', 'MEDIUM',
         '__proto__ usage detected - potential prototype pollution vulnerability'),
        
        (r'constructor\.prototype', 'prototype_pollution', 'MEDIUM',
         'Direct prototype manipulation - potential security risk'),
    ]
    
    for pattern, category, severity, message in security_patterns:
        for match in re.finditer(pattern, code, re.IGNORECASE):
            line_num = code[:match.start()].count('\n') + 1
            issues.append({
                'file': filename,
                'line': line_num,
                'column': match.start() - code[:match.start()].rfind('\n'),
                'severity': severity,
                'category': category,
                'message': message,
                'code': match.group()
            })
    
    return issues

def validate_js_with_node(code: str, filename: str) -> List[Dict]:
    """
    Validate JavaScript syntax using Node.js
    
    Args:
        code: JavaScript code to validate
        filename: Source filename
        
    Returns:
        List of syntax issues
    """
    issues = []
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Run node syntax check
        result = subprocess.run(
            ['node', '--check', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Parse output for errors
        if result.returncode != 0:
            error_lines = result.stderr.split('\n')
            for line in error_lines:
                if 'SyntaxError' in line:
                    # Extract line number from error message
                    line_match = re.search(r':(\d+)', line)
                    line_num = int(line_match.group(1)) if line_match else 1
                    
                    issues.append({
                        'file': filename,
                        'line': line_num,
                        'severity': 'HIGH',
                        'category': 'syntax_error',
                        'message': f'JavaScript syntax error: {line.strip()}',
                        'code': ''
                    })
        
        # Clean up
        os.unlink(temp_file)
        
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        # Node.js not available or other error - skip deep validation
        issues.append({
            'file': filename,
            'line': 1,
            'severity': 'LOW',
            'category': 'validation_skipped',
            'message': 'JavaScript syntax validation skipped (Node.js not available)',
            'code': ''
        })
    
    return issues

def validate_html_security(html: str, filename: str = "unknown.html") -> List[Dict]:
    """
    Validate HTML for security issues
    
    Args:
        html: HTML content to validate
        filename: Source filename
        
    Returns:
        List of security issues
    """
    issues = []
    
    security_patterns = [
        # Inline scripts without nonce
        (r'<script(?![^>]*nonce)(?![^>]*src)[^>]*>', 'inline_script', 'MEDIUM',
         'Inline script without nonce attribute - consider CSP'),
        
        # Inline event handlers
        (r'on\w+\s*=\s*[\'\"][^\'\"]*[\'\"]', 'inline_event_handler', 'LOW',
         'Inline event handler detected - potential XSS vector'),
        
        # JavaScript URLs
        (r'href\s*=\s*[\'\"]\s*javascript:', 'javascript_url', 'HIGH',
         'JavaScript URL detected - potential XSS vulnerability'),
        
        # Old HTML constructs
        (r'<iframe[^>]*>', 'iframe_usage', 'LOW',
         'iframe detected - consider security implications'),
        
        # Form without CSRF protection
        (r'<form[^>]*>(?!(?:.|\n)*csrf)', 'form_csrf_missing', 'MEDIUM',
         'Form without obvious CSRF protection'),
        
        # Mixed content
        (r'src\s*=\s*[\'"]http:', 'mixed_content', 'MEDIUM',
         'HTTP source detected - consider using HTTPS'),
        
        # Autocomplete on sensitive fields
        (r'<input[^>]*type\s*=\s*[\'"]password[\'"][^>]*autocomplete\s*=\s*[\'"]off[\'"]',
         'password_autocomplete_off', 'LOW',
         'Password autocomplete turned off - consider user experience and security tradeoffs'),
    ]
    
    for pattern, category, severity, message in security_patterns:
        for match in re.finditer(pattern, html, re.IGNORECASE):
            line_num = html[:match.start()].count('\n') + 1
            issues.append({
                'file': filename,
                'line': line_num,
                'severity': severity,
                'category': category,
                'message': message,
                'code': match.group()
            })
    
    return issues

def validate_sql_injection_risks(code: str, filename: str) -> List[Dict]:
    """
    Validate code for SQL injection risks
    
    Args:
        code: Code to validate
        filename: Source filename
        
    Returns:
        List of SQL injection risks
    """
    issues = []
    
    sql_patterns = [
        # String formatting in SQL
        (r'cursor\.execute\s*\(\s*f"[^"]*"', 'f_string_sql', 'HIGH',
         'f-string in SQL query - potential SQL injection'),
        
        (r'cursor\.execute\s*\(\s*"[^"]*"\s*%\s*', 'percent_format_sql', 'HIGH',
         'String formatting in SQL query - potential SQL injection'),
        
        (r'\.raw\s*\(\s*"[^"]*"\s*\)', 'django_raw_sql', 'MEDIUM',
         'Raw SQL query in Django - ensure proper parameterization'),
        
        (r'\.extra\s*\(\s*where\s*=', 'django_extra_where', 'MEDIUM',
         'Django extra() with where clause - potential SQL injection'),
        
        # Direct string concatenation
        (r'SELECT.*\s*\+\s*', 'string_concat_sql', 'MEDIUM',
         'String concatenation in SQL query - potential SQL injection'),
    ]
    
    for pattern, category, severity, message in sql_patterns:
        for match in re.finditer(pattern, code):
            line_num = code[:match.start()].count('\n') + 1
            issues.append({
                'file': filename,
                'line': line_num,
                'severity': severity,
                'category': category,
                'message': message,
                'code': match.group()
            })
    
    return issues

def validate_xss_vulnerabilities(code: str, filename: str, language: str = "python") -> List[Dict]:
    """
    Validate code for XSS vulnerabilities
    
    Args:
        code: Code to validate
        filename: Source filename
        language: Programming language
        
    Returns:
        List of XSS vulnerabilities
    """
    issues = []
    
    if language == "python":
        # Django template context issues
        patterns = [
            (r'render\s*\([^)]*{\s*[^}]*\|safe', 'template_safe_filter', 'HIGH',
             '|safe filter detected - potential XSS if user input is not properly sanitized'),
            
            (r'mark_safe\s*\(', 'mark_safe_usage', 'HIGH',
             'mark_safe() detected - ensure proper input validation'),
            
            (r'HttpResponse\s*\(\s*[^)]*\)', 'direct_http_response', 'MEDIUM',
             'Direct HttpResponse with user input - potential XSS'),
        ]
    elif language == "javascript":
        patterns = [
            (r'\.innerHTML\s*=', 'innerHTML_assignment', 'MEDIUM',
             'innerHTML assignment with user input - potential XSS'),
            
            (r'\.outerHTML\s*=', 'outerHTML_assignment', 'MEDIUM',
             'outerHTML assignment with user input - potential XSS'),
            
            (r'document\.write\s*\(', 'document_write', 'MEDIUM',
             'document.write() with user input - potential XSS'),
            
            (r'\.html\s*\(\s*[^)]+\)', 'jquery_html', 'MEDIUM',
             'jQuery .html() with user input - potential XSS'),
            
            (r'\.append\s*\(\s*[^)]+\)', 'jquery_append', 'LOW',
             'jQuery .append() with user input - potential XSS with careful review'),
        ]
    else:
        patterns = []
    
    for pattern, category, severity, message in patterns:
        for match in re.finditer(pattern, code):
            line_num = code[:match.start()].count('\n') + 1
            issues.append({
                'file': filename,
                'line': line_num,
                'severity': severity,
                'category': category,
                'message': message,
                'code': match.group()
            })
    
    return issues

def comprehensive_syntax_validation(file_path: str, content: str) -> Dict[str, any]:
    """
    Comprehensive syntax and security validation for a file
    
    Args:
        file_path: Path to the file
        content: File content
        
    Returns:
        Validation results
    """
    file_ext = file_path.lower().split('.')[-1]
    issues = []
    is_valid = True
    
    if file_ext == 'py':
        is_valid, py_issues = validate_python_syntax(content, file_path)
        issues.extend(py_issues)
        
        # Additional Python-specific checks
        sql_issues = validate_sql_injection_risks(content, file_path)
        issues.extend(sql_issues)
        
        xss_issues = validate_xss_vulnerabilities(content, file_path, 'python')
        issues.extend(xss_issues)
    
    elif file_ext in ['js', 'jsx']:
        is_valid, js_issues = validate_javascript_syntax(content, file_path)
        issues.extend(js_issues)
        
        xss_issues = validate_xss_vulnerabilities(content, file_path, 'javascript')
        issues.extend(xss_issues)
    
    elif file_ext == 'html':
        html_issues = validate_html_security(content, file_path)
        issues.extend(html_issues)
        is_valid = len(html_issues) == 0
    
    else:
        is_valid = True
    
    # Categorize issues by severity
    critical_issues = [issue for issue in issues if issue['severity'] == 'CRITICAL']
    high_issues = [issue for issue in issues if issue['severity'] == 'HIGH']
    medium_issues = [issue for issue in issues if issue['severity'] == 'MEDIUM']
    low_issues = [issue for issue in issues if issue['severity'] == 'LOW']
    
    return {
        'is_valid': is_valid,
        'file': file_path,
        'summary': {
            'total_issues': len(issues),
            'critical': len(critical_issues),
            'high': len(high_issues),
            'medium': len(medium_issues),
            'low': len(low_issues)
        },
        'issues': issues,
        'critical_issues': critical_issues,
        'high_issues': high_issues
    }