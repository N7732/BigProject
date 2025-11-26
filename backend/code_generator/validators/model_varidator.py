"""
Model validators for Django model generation
Cybersecurity-focused model validation
"""

import re
from typing import Dict, List, Tuple, Any
from django.core.exceptions import ValidationError

# Valid Django field types
VALID_FIELD_TYPES = {
    'CharField', 'TextField', 'IntegerField', 'BooleanField', 'DateField',
    'DateTimeField', 'EmailField', 'URLField', 'SlugField', 'DecimalField',
    'FloatField', 'ImageField', 'FileField', 'ForeignKey', 'ManyToManyField',
    'OneToOneField', 'AutoField', 'BigAutoField', 'UUIDField', 'JSONField',
    'PositiveIntegerField', 'PositiveSmallIntegerField', 'SmallIntegerField',
    'DurationField', 'TimeField', 'BinaryField', 'GenericIPAddressField'
}

# Valid field parameters
VALID_FIELD_PARAMS = {
    'max_length', 'null', 'blank', 'default', 'unique', 'primary_key',
    'choices', 'help_text', 'verbose_name', 'editable', 'db_index',
    'on_delete', 'related_name', 'to', 'upload_to', 'auto_now',
    'auto_now_add', 'max_digits', 'decimal_places'
}

# Reserved Python/Django keywords
RESERVED_KEYWORDS = {
    'class', 'def', 'import', 'from', 'as', 'return', 'if', 'else',
    'elif', 'for', 'while', 'break', 'continue', 'pass', 'in', 'is',
    'and', 'or', 'not', 'True', 'False', 'None', 'self', 'super',
    'model', 'models', 'admin', 'apps', 'views', 'urls', 'forms',
    'settings', 'manage', 'migrations', 'static', 'media', 'template'
}

# Sensitive field names that require special handling
SENSITIVE_FIELD_NAMES = {
    'password', 'secret', 'token', 'key', 'credential', 'private_key',
    'api_key', 'access_key', 'secret_key', 'auth_token', 'session_key'
}

def validate_model_name(name: str) -> Tuple[bool, str]:
    """
    Validate Django model name
    
    Args:
        name: Model name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Model name cannot be empty"
    
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
        return False, "Model name must start with a letter or underscore and contain only letters, numbers, and underscores"
    
    if name in RESERVED_KEYWORDS:
        return False, f"Model name '{name}' is a reserved keyword"
    
    if not name[0].isupper():
        return False, "Model name should start with an uppercase letter (PascalCase)"
    
    if len(name) > 100:
        return False, "Model name is too long (max 100 characters)"
    
    # Check for suspicious model names
    suspicious_patterns = ['Test', 'Demo', 'Example', 'Temp', 'Backup']
    for pattern in suspicious_patterns:
        if pattern.lower() in name.lower():
            return False, f"Model name '{name}' may indicate test or temporary code"
    
    return True, ""

def validate_field_name(name: str) -> Tuple[bool, str]:
    """
    Validate model field name
    
    Args:
        name: Field name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Field name cannot be empty"
    
    if not re.match(r'^[a-z_][a-z0-9_]*$', name):
        return False, "Field name must start with a lowercase letter or underscore and contain only lowercase letters, numbers, and underscores"
    
    if name in RESERVED_KEYWORDS:
        return False, f"Field name '{name}' is a reserved keyword"
    
    if len(name) > 50:
        return False, "Field name is too long (max 50 characters)"
    
    # Check for common field name conflicts
    conflicting_names = {'id', 'pk', 'delete', 'save', 'clean'}
    if name in conflicting_names:
        return False, f"Field name '{name}' conflicts with Django model methods"
    
    return True, ""

def validate_field_type(field_type: str) -> Tuple[bool, str]:
    """
    Validate Django field type
    
    Args:
        field_type: Field type to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not field_type:
        return False, "Field type cannot be empty"
    
    if field_type not in VALID_FIELD_TYPES:
        return False, f"Invalid field type '{field_type}'. Valid types: {', '.join(sorted(VALID_FIELD_TYPES))}"
    
    return True, ""

def validate_field_parameters(field_type: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate field parameters for a given field type
    
    Args:
        field_type: Type of field
        parameters: Dictionary of field parameters
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for invalid parameters
    for param_name in parameters.keys():
        if param_name not in VALID_FIELD_PARAMS:
            return False, f"Invalid parameter '{param_name}' for field type '{field_type}'"
    
    # Field-specific validations
    if field_type == 'CharField':
        if 'max_length' not in parameters:
            return False, "CharField requires 'max_length' parameter"
        max_length = parameters['max_length']
        if not isinstance(max_length, int) or max_length <= 0 or max_length > 5000:
            return False, "CharField max_length must be a positive integer between 1 and 5000"
    
    elif field_type in ['ForeignKey', 'ManyToManyField', 'OneToOneField']:
        if 'to' not in parameters:
            return False, f"{field_type} requires 'to' parameter (target model)"
        if field_type == 'ForeignKey' and 'on_delete' not in parameters:
            return False, "ForeignKey requires 'on_delete' parameter"
    
    elif field_type in ['DecimalField']:
        if 'max_digits' not in parameters or 'decimal_places' not in parameters:
            return False, "DecimalField requires both 'max_digits' and 'decimal_places' parameters"
        max_digits = parameters['max_digits']
        decimal_places = parameters['decimal_places']
        if not isinstance(max_digits, int) or max_digits <= 0 or max_digits > 100:
            return False, "DecimalField max_digits must be a positive integer between 1 and 100"
        if not isinstance(decimal_places, int) or decimal_places < 0 or decimal_places >= max_digits:
            return False, "DecimalField decimal_places must be a non-negative integer less than max_digits"
    
    # Security-specific validations
    if 'default' in parameters:
        default_value = parameters['default']
        if field_type in ['CharField', 'TextField'] and isinstance(default_value, str):
            if len(default_value) > 1000:
                return False, "Default value too long for text field"
    
    return True, ""

def validate_sensitive_field(field_name: str, field_type: str, parameters: Dict[str, Any]) -> List[str]:
    """
    Validate security aspects of sensitive fields
    
    Args:
        field_name: Name of the field
        field_type: Type of field
        parameters: Field parameters
        
    Returns:
        List of security warnings
    """
    warnings = []
    
    # Check if field name indicates sensitive data
    field_lower = field_name.lower()
    is_sensitive = any(sensitive in field_lower for sensitive in SENSITIVE_FIELD_NAMES)
    
    if is_sensitive:
        # Security recommendations for sensitive fields
        if field_type in ['CharField', 'TextField']:
            if parameters.get('max_length', 255) > 255:
                warnings.append(f"Sensitive field '{field_name}' has large max_length. Consider limiting storage.")
            
            if not parameters.get('blank', False):
                warnings.append(f"Sensitive field '{field_name}' is required. Consider making it optional for security.")
        
        # Check for proper field type for sensitive data
        if field_lower == 'password' and field_type != 'CharField':
            warnings.append(f"Password field '{field_name}' should use CharField with proper hashing")
        
        if 'token' in field_lower and parameters.get('max_length', 0) < 64:
            warnings.append(f"Token field '{field_name}' should have sufficient length for secure tokens")
    
    return warnings

def validate_field_definition(field_name: str, field_type: str, parameters: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
    """
    Complete validation of a field definition
    
    Args:
        field_name: Name of the field
        field_type: Type of field
        parameters: Field parameters
        
    Returns:
        Tuple of (is_valid, error_message, security_warnings)
    """
    security_warnings = []
    
    # Validate field name
    is_valid, error = validate_field_name(field_name)
    if not is_valid:
        return False, error, security_warnings
    
    # Validate field type
    is_valid, error = validate_field_type(field_type)
    if not is_valid:
        return False, error, security_warnings
    
    # Validate parameters
    is_valid, error = validate_field_parameters(field_type, parameters)
    if not is_valid:
        return False, error, security_warnings
    
    # Check for security issues with sensitive fields
    security_warnings = validate_sensitive_field(field_name, field_type, parameters)
    
    return True, "", security_warnings

def validate_model_fields(fields: List[Dict[str, Any]]) -> Tuple[bool, str, List[str]]:
    """
    Validate all fields in a model
    
    Args:
        fields: List of field definitions
        
    Returns:
        Tuple of (is_valid, error_message, security_warnings)
    """
    if not fields:
        return False, "Model must have at least one field", []
    
    field_names = set()
    all_security_warnings = []
    
    for field in fields:
        field_name = field.get('name')
        
        # Check for duplicate field names
        if field_name in field_names:
            return False, f"Duplicate field name: '{field_name}'", []
        field_names.add(field_name)
        
        # Validate individual field
        is_valid, error, security_warnings = validate_field_definition(
            field_name,
            field.get('type'),
            field.get('parameters', {})
        )
        if not is_valid:
            return False, error, []
        
        all_security_warnings.extend(security_warnings)
    
    # Check for missing common fields
    common_fields = ['created_at', 'updated_at']
    missing_common = [field for field in common_fields if field not in field_names]
    if missing_common:
        all_security_warnings.append(f"Consider adding common fields: {', '.join(missing_common)}")
    
    return True, "", all_security_warnings

def validate_model_for_security(model_name: str, fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Comprehensive security validation for a model
    
    Args:
        model_name: Name of the model
        fields: List of field definitions
        
    Returns:
        Security validation results
    """
    results = {
        'model_name': model_name,
        'is_valid': False,
        'errors': [],
        'warnings': [],
        'security_score': 0
    }
    
    # Validate model name
    is_valid, error = validate_model_name(model_name)
    if not is_valid:
        results['errors'].append(error)
        return results
    
    # Validate fields
    is_valid, error, warnings = validate_model_fields(fields)
    if not is_valid:
        results['errors'].append(error)
        return results
    
    results['is_valid'] = True
    results['warnings'] = warnings
    
    # Calculate security score
    total_fields = len(fields)
    sensitive_fields = sum(1 for field in fields if any(
        sensitive in field.get('name', '').lower() for sensitive in SENSITIVE_FIELD_NAMES
    ))
    
    # Base score
    security_score = 100
    
    # Penalize for sensitive fields without proper handling
    if sensitive_fields > 0:
        security_score -= sensitive_fields * 10
    
    # Penalize for too many fields (potential data exposure)
    if total_fields > 20:
        security_score -= 10
    
    # Penalize for warnings
    security_score -= len(warnings) * 5
    
    results['security_score'] = max(0, security_score)
    
    return results