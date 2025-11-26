#!/usr/bin/env python3
"""
Test script to verify the security validator works
"""

import os
import sys
import tempfile
import json
from pathlib import Path

def create_test_project():
    """Create a test project with both secure and insecure code"""
    test_dir = tempfile.mkdtemp(prefix="test_project_")
    print(f"📁 Creating test project in: {test_dir}")
    
    # Create project structure
    os.makedirs(os.path.join(test_dir, 'backend'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'frontend'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'templates'), exist_ok=True)
    
    # Create test files with SECURITY ISSUES (for testing)
    
    # 1. Django settings with issues
    settings_content = '''
DEBUG = True  # INSECURE: Debug enabled
SECRET_KEY = 'weak-key'  # INSECURE: Weak secret key
ALLOWED_HOSTS = ['*']  # INSECURE: All hosts allowed

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'PASSWORD': 'hardcoded_password'  # INSECURE: Hardcoded password
    }
}

# Missing security headers
# SECURE_HSTS_SECONDS = 31536000
# SESSION_COOKIE_SECURE = True
'''
    
    with open(os.path.join(test_dir, 'settings.py'), 'w') as f:
        f.write(settings_content)
    
    # 2. Python file with security issues
    views_content = '''
import os
import pickle
from django.http import HttpResponse
import subprocess

def vulnerable_view(request):
    # INSECURE: SQL injection risk
    user_input = request.GET.get('query')
    cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
    
    # INSECURE: Command injection
    filename = request.GET.get('file')
    os.system(f"cat {filename}")
    
    # INSECURE: Unsafe deserialization
    data = pickle.loads(request.GET.get('data'))
    
    # INSECURE: Hardcoded secret
    api_key = "sk_live_1234567890"
    
    return HttpResponse("Vulnerable view")

def xss_view(request):
    # INSECURE: Potential XSS
    user_content = request.GET.get('content')
    return HttpResponse(f"<div>{user_content}</div>")
'''
    
    with open(os.path.join(test_dir, 'views.py'), 'w') as f:
        f.write(views_content)
    
    # 3. JavaScript with security issues
    react_content = '''
function VulnerableComponent() {
    // INSECURE: XSS risk
    const userHtml = props.userContent;
    document.getElementById('content').innerHTML = userHtml;
    
    // INSECURE: eval usage
    const userCode = localStorage.getItem('userScript');
    eval(userCode);
    
    // INSECURE: localStorage with sensitive data
    localStorage.setItem('password', 'myPassword123');
    
    return React.createElement('div', {
        dangerouslySetInnerHTML: { __html: userHtml }
    });
}
'''
    
    os.makedirs(os.path.join(test_dir, 'frontend', 'src'), exist_ok=True)
    with open(os.path.join(test_dir, 'frontend', 'src', 'App.js'), 'w') as f:
        f.write(react_content)
    
    # 4. HTML with security issues
    html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <!-- INSECURE: Form without CSRF -->
    <form action="/submit" method="POST">
        <input type="text" name="data">
        <input type="submit">
    </form>
    
    <!-- INSECURE: Inline script -->
    <script>
        var apiKey = "hardcoded_key_123";
        document.write("<div>Welcome " + userInput + "</div>");
    </script>
    
    <!-- INSECURE: JavaScript URL -->
    <a href="javascript:alert('xss')">Click me</a>
</body>
</html>
'''
    
    with open(os.path.join(test_dir, 'templates', 'index.html'), 'w') as f:
        f.write(html_content)
    
    # 5. Requirements with vulnerable packages
    requirements_content = '''
Django==2.0.0  # VULNERABLE: Old version with known CVEs
requests==2.0.0  # VULNERABLE: Old version
pillow==5.0.0  # VULNERABLE: Old version
django-auth==1.0.0  # SUSPICIOUS: Potential typosquatting
'''
    
    with open(os.path.join(test_dir, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)
    
    # 6. Create context file
    context = {
        "project_name": "test_project",
        "secret_key": "weak-secret-key-for-testing",
        "description": "Test project for security validation",
        "author": "Test User",
        "database": {
            "engine": "django.db.backends.sqlite3",
            "name": "test.db",
            "password": "test123"
        }
    }
    
    context_file = os.path.join(test_dir, 'test_context.json')
    with open(context_file, 'w') as f:
        json.dump(context, f, indent=2)
    
    return test_dir, context_file

def run_validation_test():
    """Run the security validation on test project"""
    print("🚀 STARTING SECURITY VALIDATION TEST")
    print("=" * 50)
    
    # Create test project
    test_dir, context_file = create_test_project()
    
    # Run validation
    validator_path = os.path.join('code_generator', 'validate_project.py')
    
    if not os.path.exists(validator_path):
        print(f"❌ Validator not found at: {validator_path}")
        return False
    
    import subprocess
    
    cmd = [
        sys.executable,
        validator_path,
        test_dir,
        '--context-file', context_file,
        '--min-score', '70',
        '--output', os.path.join(test_dir, 'security_test_report.json')
    ]
    
    print(f"🔧 Running: {' '.join(cmd)}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        # Check if report was generated
        report_file = os.path.join(test_dir, 'security_test_report.json')
        if os.path.exists(report_file):
            print(f"✅ Report generated: {report_file}")
            
            # Load and analyze report
            with open(report_file, 'r') as f:
                report = json.load(f)
            
            print("\n📊 TEST RESULTS ANALYSIS:")
            print(f"   Security Score: {report['summary']['security_score']}/100")
            print(f"   Critical Issues: {report['summary']['critical_issues']}")
            print(f"   Total Issues: {report['summary']['total_issues']}")
            
            # Verify vulnerabilities were detected
            critical_issues = report['security_scan'].get('critical_issues', [])
            expected_issues = [
                'hardcoded secret', 'DEBUG = True', 'Weak secret key',
                'SQL injection', 'eval() function', 'pickle.loads'
            ]
            
            detected_issues = []
            for issue in critical_issues:
                detected_issues.append(issue['message'])
                print(f"   - {issue['message']}")
            
            # Check if expected issues were found
            found_count = 0
            for expected in expected_issues:
                if any(expected.lower() in msg.lower() for msg in detected_issues):
                    found_count += 1
                    print(f"   ✅ Detected: {expected}")
                else:
                    print(f"   ❌ Missed: {expected}")
            
            print(f"\n🎯 Detection Rate: {found_count}/{len(expected_issues)}")
            
            if found_count >= 3:  # At least 3 of 6 expected issues
                print("🎉 VALIDATION TEST PASSED! Security issues were properly detected.")
                return True
            else:
                print("❌ VALIDATION TEST FAILED! Many security issues were missed.")
                return False
        else:
            print("❌ No report file generated")
            return False
            
    except Exception as e:
        print(f"❌ Error running validation: {e}")
        return False
    finally:
        # Cleanup
        print(f"\n🧹 Test files are in: {test_dir}")
        print("   (This directory will not be automatically deleted for inspection)")

if __name__ == "__main__":
    success = run_validation_test()
    sys.exit(0 if success else 1)