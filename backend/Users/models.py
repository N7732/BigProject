from django.db import models
from django.contrib.auth.models import AbstractUser
from code_generator.validators import basic_validator, dependency_checker
# Create your models here.
class userinform(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')), null=True, blank=True)

    def __str__(self):
        return self.username
    
def validate_user_code(self, code: str, filename: str) -> bool:
    """Validate user-submitted code for security issues."""
    try:
        is_valid, issues = basic_validator.validate_python_syntax(code, filename)
        if not is_valid:
            for issue in issues:
                print(f"Security Issue: {issue['message']} at line {issue['line']}")
            return False
        return True
    except Exception as e:
        print(f"Validation error: {e}")
        return False
    
def check_user_dependencies(self, dependencies: dict) -> bool:
    """Check user-submitted dependencies for known vulnerabilities."""
    try:
        vulnerabilities = dependency_checker.check_vulnerable_dependencies(dependencies)
        if vulnerabilities:
            for pkg, issues in vulnerabilities.items():
                for issue in issues:
                    print(f"Vulnerability in {pkg}: {issue['description']}")
            return False
        return True
    except Exception as e:
        print(f"Dependency check error: {e}")
        return False
    