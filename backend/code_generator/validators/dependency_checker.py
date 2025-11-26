"""
Dependency security checker for AI-generated code
Cybersecurity-focused dependency validation
"""

import re
import json
import requests
from typing import Dict, List, Tuple, Set, Any
from packaging import version
import warnings
import os

# Known vulnerable packages and versions (expanded list)
VULNERABLE_PACKAGES = {
    'django': {
        '<2.2.0': 'CVE-2019-19844 - Potential SQL injection',
        '<3.0.0': 'CVE-2020-9404 - GIS SQL injection',
        '<3.2.0': 'CVE-2021-33203 - Directory traversal',
        '<3.2.5': 'CVE-2021-45452 - Directory traversal',
    },
    'react': {
        '<16.14.0': 'CVE-2020-15187 - XSS vulnerability',
        '<17.0.2': 'CVE-2021-26866 - Prototype pollution',
    },
    'react-dom': {
        '<16.14.0': 'CVE-2020-15187 - XSS vulnerability',
        '<17.0.2': 'CVE-2021-26866 - Prototype pollution',
    },
    'axios': {
        '<0.21.1': 'CVE-2020-28168 - SSRF vulnerability',
    },
    'express': {
        '<4.17.0': 'CVE-2020-15104 - Prototype pollution',
    },
    'sqlparse': {
        '<0.4.0': 'CVE-2021-32839 - SQL injection',
    },
    'pillow': {
        '<8.0.0': 'Multiple CVEs in image processing',
        '<9.0.0': 'CVE-2022-22817 - Buffer overflow',
    },
    'cryptography': {
        '<3.3.0': 'CVE-2020-25659 - Timing attack',
    },
    'requests': {
        '<2.25.0': 'CVE-2020-26137 - HTTP header injection',
    },
    'urllib3': {
        '<1.26.0': 'CVE-2020-26137 - HTTP header injection',
    },
    'pyyaml': {
        '<5.4': 'CVE-2020-1747 - Code execution',
    },
    'jinja2': {
        '<2.11.3': 'CVE-2020-28493 - SQL injection',
    }
}

# Malicious packages (known typosquatting) - expanded list
MALICIOUS_PACKAGES = {
    'django-auth', 'django-admin', 'django-models', 'django-utils',
    'django-secure', 'django-security', 'django-setup',
    'react-dom', 'react-router', 'axios-http', 'express-server',
    'python-dateutil', 'requests-http', 'crypto-js', 'node-fetch',
    'py-requests', 'python-requests', 'request', 'requrests',
    'cryptography', 'crypto', 'pycrypto', 'pycryptodome',
    'selenium', 'bs4', 'beautifulsoup', 'lxml'
}

# Packages with restrictive licenses
RESTRICTIVE_LICENSES = {
    'AGPL', 'GPL-3.0', 'SSPL', 'CC-BY-NC-4.0'
}

# Security-focused packages (recommended)
SECURITY_PACKAGES = {
    'bcrypt', 'cryptography', 'passlib', 'pyjwt', 'authlib',
    'django-csp', 'django-axes', 'django-ratelimit'
}

def check_vulnerable_dependencies(dependencies: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Check dependencies for known vulnerabilities
    
    Args:
        dependencies: Dict of package_name -> version_spec
        
    Returns:
        Dict of vulnerabilities by package
    """
    vulnerabilities = {}
    
    for package, version_spec in dependencies.items():
        package_lower = package.lower()
        
        # Check against known vulnerable packages
        if package_lower in VULNERABLE_PACKAGES:
            for vulnerable_version, description in VULNERABLE_PACKAGES[package_lower].items():
                try:
                    # Extract version from spec (handle ~=, >=, etc.)
                    clean_version = extract_version_from_spec(version_spec)
                    if clean_version and is_version_vulnerable(clean_version, vulnerable_version):
                        if package not in vulnerabilities:
                            vulnerabilities[package] = []
                        vulnerabilities[package].append({
                            'description': description,
                            'vulnerable_version': vulnerable_version,
                            'current_version': clean_version
                        })
                except Exception as e:
                    # If version parsing fails, flag for manual review
                    if package not in vulnerabilities:
                        vulnerabilities[package] = []
                    vulnerabilities[package].append({
                        'description': f"Version parsing error: {str(e)}",
                        'vulnerable_version': 'unknown',
                        'current_version': version_spec
                    })
    
    return vulnerabilities

def extract_version_from_spec(version_spec: str) -> str:
    """
    Extract version number from version specifier
    
    Args:
        version_spec: Version specification string
        
    Returns:
        Clean version string
    """
    # Remove specifiers and extract version
    clean_spec = re.sub(r'[~=<>!]=?', '', version_spec).strip()
    
    # Handle complex specifiers by taking the first version
    if ',' in clean_spec:
        clean_spec = clean_spec.split(',')[0].strip()
    
    # Extract version pattern (major.minor.patch)
    version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', clean_spec)
    if version_match:
        return version_match.group(1)
    
    return clean_spec

def is_version_vulnerable(current_version: str, vulnerable_spec: str) -> bool:
    """
    Check if current version matches vulnerable specification
    
    Args:
        current_version: Current package version
        vulnerable_spec: Vulnerable version specification
        
    Returns:
        Boolean indicating if vulnerable
    """
    try:
        if not current_version or current_version == 'latest':
            return True  # Assume vulnerable if no specific version
        
        current = version.parse(current_version)
        
        if vulnerable_spec.startswith('<='):
            vulnerable_ver = version.parse(vulnerable_spec[2:])
            return current <= vulnerable_ver
        elif vulnerable_spec.startswith('<'):
            vulnerable_ver = version.parse(vulnerable_spec[1:])
            return current < vulnerable_ver
        elif vulnerable_spec.startswith('>='):
            vulnerable_ver = version.parse(vulnerable_spec[2:])
            return current >= vulnerable_ver
        elif vulnerable_spec.startswith('>'):
            vulnerable_ver = version.parse(vulnerable_spec[1:])
            return current > vulnerable_ver
        elif vulnerable_spec.startswith('=='):
            vulnerable_ver = version.parse(vulnerable_spec[2:])
            return current == vulnerable_ver
        
        return False
    except Exception as e:
        print(f"Version comparison error: {e}")
        return True  # Assume vulnerable on error

def validate_dependency_versions(dependencies: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Validate dependency versions for security best practices
    
    Args:
        dependencies: Dict of package_name -> version_spec
        
    Returns:
        Dict of recommendations by package
    """
    recommendations = {}
    
    for package, version_spec in dependencies.items():
        package_lower = package.lower()
        warnings = []
        
        # Check for overly permissive version specifiers
        if version_spec in ['*', 'latest', '']:
            warnings.append(f"Overly permissive version specifier: '{version_spec}'. Use exact version.")
        
        # Check for vulnerable version ranges
        if '>' in version_spec and '<' not in version_spec:
            warnings.append("Unbounded upper version range. Specify maximum version.")
        
        # Check for pre-release versions in production
        if any(term in version_spec.lower() for term in ['alpha', 'beta', 'rc', 'dev', 'pre']):
            warnings.append("Pre-release version detected. Not recommended for production.")
        
        # Check for outdated major versions
        if package_lower == 'django' and version_spec.startswith('2.'):
            warnings.append("Consider upgrading to Django 3.x or 4.x for LTS support and security updates")
        
        if package_lower == 'react' and version_spec.startswith('16.'):
            warnings.append("Consider upgrading to React 17.x or 18.x for latest features and security")
        
        # Check for missing security packages
        if package_lower in ['django'] and 'bcrypt' not in dependencies:
            warnings.append("Consider adding bcrypt for secure password hashing")
        
        if warnings:
            recommendations[package] = warnings
    
    return recommendations

def scan_for_malicious_packages(dependencies: Dict[str, str]) -> List[Dict]:
    """
    Scan for potentially malicious packages (typosquatting)
    
    Args:
        dependencies: Dict of package_name -> version_spec
        
    Returns:
        List of potentially malicious packages
    """
    suspicious = []
    
    for package in dependencies.keys():
        package_lower = package.lower()
        
        # Check for typosquatting
        if package_lower in MALICIOUS_PACKAGES:
            suspicious.append({
                'package': package,
                'issue': 'potential_typosquatting',
                'message': f"Potential typosquatting: {package}"
            })
        
        # Check for suspicious patterns
        suspicious_patterns = [
            (r'.*test.*', 'suspicious_name_test'),
            (r'.*demo.*', 'suspicious_name_demo'),
            (r'.*example.*', 'suspicious_name_example'),
            (r'.*fake.*', 'suspicious_name_fake'),
            (r'.*malicious.*', 'suspicious_name_malicious'),
            (r'.*hack.*', 'suspicious_name_hack'),
            (r'.*exploit.*', 'suspicious_name_exploit'),
            (r'.*backdoor.*', 'suspicious_name_backdoor'),
            (r'.*keylogger.*', 'suspicious_name_keylogger'),
        ]
        
        for pattern, issue_type in suspicious_patterns:
            if re.match(pattern, package_lower, re.IGNORECASE):
                suspicious.append({
                    'package': package,
                    'issue': issue_type,
                    'message': f"Suspicious package name: {package}"
                })
                break
        
        # Check for recently created packages with high version numbers
        if any(char.isdigit() for char in package) and len(package) > 15:
            suspicious.append({
                'package': package,
                'issue': 'suspicious_name_numbers',
                'message': f"Suspicious package name with numbers: {package}"
            })
        
        # Check for names too similar to popular packages
        popular_packages = ['requests', 'django', 'react', 'axios', 'express']
        for popular in popular_packages:
            if popular in package_lower and package_lower != popular:
                if len(package_lower) - len(popular) <= 2:
                    suspicious.append({
                        'package': package,
                        'issue': 'similar_to_popular',
                        'message': f"Package name very similar to popular package '{popular}': {package}"
                    })
    
    return suspicious

def check_license_compliance(dependencies: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Check dependency licenses for compliance issues
    
    Args:
        dependencies: Dict of package_name -> version_spec
        
    Returns:
        Dict of license issues by package
    """
    license_issues = {}
    
    # This would typically integrate with a license database
    # For demonstration, we'll use a static list
    known_licenses = {
        'django': 'BSD-3-Clause',
        'react': 'MIT',
        'react-dom': 'MIT',
        'axios': 'MIT',
        'express': 'MIT',
        'pillow': 'HPND',
        'cryptography': 'Apache-2.0 OR BSD-3-Clause',
        'requests': 'Apache-2.0',
        'bcrypt': 'Apache-2.0',
        'pyjwt': 'MIT',
        'django-csp': 'MIT',
        'django-axes': 'MIT',
    }
    
    for package in dependencies.keys():
        package_lower = package.lower()
        
        if package_lower in known_licenses:
            license_type = known_licenses[package_lower]
            
            if license_type in RESTRICTIVE_LICENSES:
                if package not in license_issues:
                    license_issues[package] = []
                license_issues[package].append(
                    f"Restrictive license: {license_type}. "
                    f"Ensure compliance with your project's license."
                )
        else:
            # Unknown license - flag for review
            if package not in license_issues:
                license_issues[package] = []
            license_issues[package].append(
                "Unknown license. Manual review required."
            )
    
    return license_issues

def check_security_package_recommendations(dependencies: Dict[str, str]) -> List[str]:
    """
    Recommend security-focused packages based on project dependencies
    
    Args:
        dependencies: Dict of package_name -> version_spec
        
    Returns:
        List of security package recommendations
    """
    recommendations = []
    project_deps = set(dependencies.keys())
    
    # Django projects
    if any('django' in dep.lower() for dep in project_deps):
        security_packages = {
            'bcrypt': 'Secure password hashing',
            'django-axes': 'Brute force protection',
            'django-csp': 'Content Security Policy',
            'django-ratelimit': 'Rate limiting',
            'pyjwt': 'JWT token handling'
        }
        
        for pkg, description in security_packages.items():
            if pkg not in project_deps:
                recommendations.append(f"Consider adding {pkg} for {description}")
    
    # React projects
    if any('react' in dep.lower() for dep in project_deps):
        recommendations.extend([
            "Consider adding DOMPurify for HTML sanitization",
            "Consider adding helmet for security headers",
            "Consider adding crypto-js for cryptographic operations"
        ])
    
    return recommendations

def comprehensive_dependency_scan(dependencies: Dict[str, str]) -> Dict[str, any]:
    """
    Comprehensive dependency security scan
    
    Args:
        dependencies: Dict of package_name -> version_spec
        
    Returns:
        Comprehensive scan results
    """
    vulnerabilities = check_vulnerable_dependencies(dependencies)
    version_recommendations = validate_dependency_versions(dependencies)
    malicious_packages = scan_for_malicious_packages(dependencies)
    license_issues = check_license_compliance(dependencies)
    security_recommendations = check_security_package_recommendations(dependencies)
    
    return {
        'vulnerabilities': vulnerabilities,
        'version_recommendations': version_recommendations,
        'malicious_packages': malicious_packages,
        'license_issues': license_issues,
        'security_recommendations': security_recommendations,
        'summary': {
            'total_dependencies': len(dependencies),
            'vulnerable_packages': len(vulnerabilities),
            'suspicious_packages': len(malicious_packages),
            'license_issues_count': len(license_issues),
            'security_score': calculate_dependency_security_score(
                len(dependencies),
                len(vulnerabilities),
                len(malicious_packages)
            )
        }
    }

def calculate_dependency_security_score(total_deps: int, vulnerable: int, suspicious: int) -> int:
    """
    Calculate dependency security score (0-100)
    
    Args:
        total_deps: Total number of dependencies
        vulnerable: Number of vulnerable packages
        suspicious: Number of suspicious packages
        
    Returns:
        Security score (0-100)
    """
    if total_deps == 0:
        return 100
    
    base_score = 100
    # Penalize for vulnerabilities and suspicious packages
    score = base_score - (vulnerable * 20) - (suspicious * 30)
    
    # Penalize for having too many dependencies
    if total_deps > 50:
        score -= 10
    elif total_deps > 100:
        score -= 20
    
    return max(0, min(100, score))

def validate_requirements_file(requirements_path: str) -> Dict[str, any]:
    """
    Validate a requirements.txt file for security issues
    
    Args:
        requirements_path: Path to requirements.txt file
        
    Returns:
        Validation results
    """
    if not os.path.exists(requirements_path):
        return {'error': 'Requirements file not found'}
    
    dependencies = {}
    try:
        with open(requirements_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    # Parse package and version
                    if '==' in line:
                        pkg, ver = line.split('==', 1)
                        dependencies[pkg.strip()] = ver.strip()
                    elif '>=' in line:
                        pkg, ver = line.split('>=', 1)
                        dependencies[pkg.strip()] = f">={ver.strip()}"
                    else:
                        # Unpinned dependency
                        dependencies[line] = 'unpinned'
    
    except Exception as e:
        return {'error': f'Error parsing requirements file: {str(e)}'}
    
    return comprehensive_dependency_scan(dependencies)