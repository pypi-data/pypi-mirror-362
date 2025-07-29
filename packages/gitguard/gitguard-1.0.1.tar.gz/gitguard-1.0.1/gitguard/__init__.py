"""
GitGuard - Enterprise-Grade Secure Git Workflow
Part of Project Himalaya - AI-Human Collaborative Development Framework

A comprehensive security system that automatically validates, fixes, and audits
security issues in git repositories while maintaining development efficiency.

Key Features:
- Automatic security validation before commits
- Intelligent remediation of security issues  
- Comprehensive audit logging for compliance
- Git history protection and cleaning
- Zero-friction workflow integration

Project Creator: Herbert J. Bowers
Technical Implementation: Claude (Anthropic) - 99.99% of code, design, and documentation
License: MIT
Version: 1.0.0

This project demonstrates the potential of AI-human collaboration in creating
enterprise-grade security solutions as part of the broader Project Himalaya framework.
"""

__version__ = "1.0.1"
__author__ = "Herbert J. Bowers (Project Creator), Claude (Anthropic) - Technical Implementation"
__email__ = "HimalayaProject1@gmail.com"
__license__ = "MIT"

# Core imports for easy access
from .validator import SecurityValidator
from .config import GitGuardConfig

# Exception classes
from .exceptions import (
    GitGuardError,
    SecurityValidationError,
    ConfigurationError
)

# Main API classes
__all__ = [
    # Core classes
    "SecurityValidator",
    "GitGuardConfig",
    
    # Exceptions
    "GitGuardError",
    "SecurityValidationError", 
    "ConfigurationError",
    
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]

# Package metadata
PACKAGE_NAME = "gitguard"
DESCRIPTION = "Enterprise-grade secure git workflow system"
HOMEPAGE = "https://github.com/herbbowers/gitguard"
DOCUMENTATION = "https://gitguard.dev"

# Supported Python versions
PYTHON_REQUIRES = ">=3.8"

# Security patterns version (for updates)
PATTERNS_VERSION = "1.0.0"

def get_version():
    """Get the current GitGuard version."""
    return __version__

def get_info():
    """Get comprehensive package information."""
    return {
        "name": PACKAGE_NAME,
        "version": __version__,
        "description": DESCRIPTION,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "homepage": HOMEPAGE,
        "documentation": DOCUMENTATION,
        "python_requires": PYTHON_REQUIRES,
        "patterns_version": PATTERNS_VERSION,
    }