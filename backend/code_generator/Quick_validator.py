#!/usr/bin/env python3
"""
Quick smoke test for validators
"""

import sys
import os

def test_imports():
    """Test that all validator modules can be imported"""
    print("🔍 Testing validator imports...")
    
    try:
        # Test core imports
        from code_generator.validators.dependency_checker import check_vulnerable_dependencies
        from code_generator.validators.security_scanner import SecurityScanner
        from code_generator.validators.syntax_validator import validate_python_syntax
        
        print("✅ All core validators imported successfully")
        
        # Test comprehensive validation
        from code_generator.validators import validate_complete_project
        print("✅ Comprehensive validator imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_validation():
    """Test basic validation functionality"""
    print("\n🔍 Testing basic validation...")
    
    try:
        from code_generator.validators.syntax_validator import validate_python_syntax
        
        # Test with vulnerable code
        vulnerable_code = """
password = "hardcoded123"
secret_key = "weak_key"
eval("print('dangerous')")
"""
        
        is_valid, issues = validate_python_syntax(vulnerable_code, "test.py")
        
        if not is_valid and len(issues) > 0:
            print(f"✅ Security issues detected: {len(issues)}")
            for issue in issues[:2]:  # Show first 2
                print(f"   - {issue['message']}")
            return True
        else:
            print("❌ No security issues detected in vulnerable code")
            return False
            
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False

def test_dependency_checker():
    """Test dependency vulnerability detection"""
    print("\n🔍 Testing dependency checker...")
    
    try:
        from code_generator.validators.dependency_checker import check_vulnerable_dependencies
        
        # Test with vulnerable dependencies
        dependencies = {
            'Django': '2.0.0',  # Known vulnerable
            'requests': '2.0.0',  # Known vulnerable
            'secure-package': '1.0.0'  # Should be fine
        }
        
        vulnerabilities = check_vulnerable_dependencies(dependencies)
        
        if vulnerabilities:
            print(f"✅ Vulnerable dependencies detected: {len(vulnerabilities)}")
            for pkg, issues in vulnerabilities.items():
                print(f"   - {pkg}: {len(issues)} issues")
            return True
        else:
            print("❌ No vulnerable dependencies detected")
            return False
            
    except Exception as e:
        print(f"❌ Dependency test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 RUNNING QUICK SMOKE TEST")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_basic_validation,
        test_dependency_checker
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 RESULTS: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 ALL TESTS PASSED! Validators are working correctly.")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED! Check the implementation.")
        sys.exit(1)