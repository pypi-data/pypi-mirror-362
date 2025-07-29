# File: exceptions.py
# Path: gitguard/exceptions.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-14
# Last Modified: 2025-07-14  12:47PM
"""
GitGuard Exception Classes
Custom exceptions for better error handling and user experience.
"""

class GitGuardError(Exception):
    """Base exception class for all GitGuard errors"""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "GITGUARD_ERROR"
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.details:
            detail_str = ", ".join([f"{k}={v}" for k, v in self.details.items()])
            return f"{self.message} (Details: {detail_str})"
        return self.message

class SecurityValidationError(GitGuardError):
    """Raised when security validation fails"""
    
    def __init__(self, message: str, issues_found: int = 0, critical_issues: int = 0):
        super().__init__(
            message,
            error_code="SECURITY_VALIDATION_FAILED",
            details={
                "issues_found": issues_found,
                "critical_issues": critical_issues
            }
        )
        self.issues_found = issues_found
        self.critical_issues = critical_issues

class RemediationError(GitGuardError):
    """Raised when automatic remediation fails"""
    
    def __init__(self, message: str, operation: str = None, file_path: str = None):
        super().__init__(
            message,
            error_code="REMEDIATION_FAILED",
            details={
                "operation": operation,
                "file_path": file_path
            }
        )
        self.operation = operation
        self.file_path = file_path

class AuditError(GitGuardError):
    """Raised when audit logging fails"""
    
    def __init__(self, message: str, log_type: str = None):
        super().__init__(
            message,
            error_code="AUDIT_FAILED",
            details={"log_type": log_type}
        )
        self.log_type = log_type

class ConfigurationError(GitGuardError):
    """Raised when configuration is invalid or missing"""
    
    def __init__(self, message: str, config_file: str = None, setting: str = None):
        super().__init__(
            message,
            error_code="CONFIGURATION_ERROR",
            details={
                "config_file": config_file,
                "setting": setting
            }
        )
        self.config_file = config_file
        self.setting = setting

class GitRepositoryError(GitGuardError):
    """Raised when git repository operations fail"""
    
    def __init__(self, message: str, git_command: str = None, return_code: int = None):
        super().__init__(
            message,
            error_code="GIT_REPOSITORY_ERROR",
            details={
                "git_command": git_command,
                "return_code": return_code
            }
        )
        self.git_command = git_command
        self.return_code = return_code

class PolicyViolationError(GitGuardError):
    """Raised when security policy is violated"""
    
    def __init__(self, message: str, policy_name: str = None, violation_type: str = None):
        super().__init__(
            message,
            error_code="POLICY_VIOLATION",
            details={
                "policy_name": policy_name,
                "violation_type": violation_type
            }
        )
        self.policy_name = policy_name
        self.violation_type = violation_type

class InstallationError(GitGuardError):
    """Raised when GitGuard installation or setup fails"""
    
    def __init__(self, message: str, component: str = None):
        super().__init__(
            message,
            error_code="INSTALLATION_ERROR",
            details={"component": component}
        )
        self.component = component

class PermissionError(GitGuardError):
    """Raised when insufficient permissions for operation"""
    
    def __init__(self, message: str, required_permission: str = None, file_path: str = None):
        super().__init__(
            message,
            error_code="PERMISSION_ERROR",
            details={
                "required_permission": required_permission,
                "file_path": file_path
            }
        )
        self.required_permission = required_permission
        self.file_path = file_path

# Error code mappings for programmatic handling
ERROR_CODES = {
    "GITGUARD_ERROR": GitGuardError,
    "SECURITY_VALIDATION_FAILED": SecurityValidationError,
    "REMEDIATION_FAILED": RemediationError,
    "AUDIT_FAILED": AuditError,
    "CONFIGURATION_ERROR": ConfigurationError,
    "GIT_REPOSITORY_ERROR": GitRepositoryError,
    "POLICY_VIOLATION": PolicyViolationError,
    "INSTALLATION_ERROR": InstallationError,
    "PERMISSION_ERROR": PermissionError,
}

def get_exception_by_code(error_code: str) -> type:
    """Get exception class by error code"""
    return ERROR_CODES.get(error_code, GitGuardError)