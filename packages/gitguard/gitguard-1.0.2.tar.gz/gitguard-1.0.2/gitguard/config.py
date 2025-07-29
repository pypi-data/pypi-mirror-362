# File: config.py
# Path: gitguard/config.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-14
# Last Modified: 2025-07-14  12:48PM
"""
GitGuard Configuration Management
Handles configuration loading, validation, and default settings.
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

from .exceptions import ConfigurationError

@dataclass
class SecurityConfig:
    """Security validation configuration"""
    block_on_critical: bool = True
    block_on_high: bool = False
    auto_fix_enabled: bool = True
    scan_file_contents: bool = True
    max_file_size_mb: int = 1
    custom_patterns: List[str] = None
    
    def __post_init__(self):
        if self.custom_patterns is None:
            self.custom_patterns = []

@dataclass
class AuditConfig:
    """Audit logging configuration"""
    enabled: bool = True
    retention_days: int = 90
    log_format: str = "json"
    include_content: bool = False
    compress_old_logs: bool = True

@dataclass
class RemediationConfig:
    """Remediation behavior configuration"""
    interactive_mode: bool = True
    create_backups: bool = True
    clean_git_history: bool = True
    update_gitignore: bool = True
    remove_files: bool = False

@dataclass
class NotificationConfig:
    """Notification settings"""
    slack_webhook: Optional[str] = None
    email_alerts: bool = False
    console_notifications: bool = True

@dataclass
class IntegrationConfig:
    """External system integrations"""
    github_checks: bool = False
    jira_project: Optional[str] = None
    ci_cd_integration: bool = False

class GitGuardConfig:
    """Main GitGuard configuration class"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = self._find_config_file(config_path)
        self.config_data = {}
        
        # Initialize with defaults
        self.security = SecurityConfig()
        self.audit = AuditConfig()
        self.remediation = RemediationConfig()
        self.notification = NotificationConfig()
        self.integration = IntegrationConfig()
        
        # Load configuration if file exists
        if self.config_path and self.config_path.exists():
            self.load_config()
    
    def _find_config_file(self, config_path: Optional[str] = None) -> Optional[Path]:
        """Find configuration file in standard locations"""
        if config_path:
            path = Path(config_path)
            if not path.exists():
                raise ConfigurationError(f"Configuration file not found: {config_path}")
            return path
        
        # Search standard locations
        search_paths = [
            Path.cwd() / ".gitguard.yaml",
            Path.cwd() / ".gitguard.yml", 
            Path.cwd() / "gitguard.yaml",
            Path.cwd() / "gitguard.yml",
            Path.home() / ".gitguard" / "config.yaml",
            Path.home() / ".config" / "gitguard" / "config.yaml",
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        return None
    
    def load_config(self):
        """Load configuration from file"""
        if not self.config_path or not self.config_path.exists():
            return
        
        try:
            with open(self.config_path, 'r') as f:
                if self.config_path.suffix.lower() in ['.yaml', '.yml']:
                    self.config_data = yaml.safe_load(f) or {}
                elif self.config_path.suffix.lower() == '.json':
                    self.config_data = json.load(f)
                else:
                    raise ConfigurationError(f"Unsupported config file format: {self.config_path.suffix}")
        
        except Exception as e:
            raise ConfigurationError(f"Failed to load config file: {str(e)}", str(self.config_path))
        
        # Update configuration objects
        self._update_from_dict()
    
    def _update_from_dict(self):
        """Update configuration objects from loaded data"""
        # Security configuration
        if 'security' in self.config_data:
            security_data = self.config_data['security']
            self.security = SecurityConfig(
                block_on_critical=security_data.get('block_on_critical', self.security.block_on_critical),
                block_on_high=security_data.get('block_on_high', self.security.block_on_high),
                auto_fix_enabled=security_data.get('auto_fix_enabled', self.security.auto_fix_enabled),
                scan_file_contents=security_data.get('scan_file_contents', self.security.scan_file_contents),
                max_file_size_mb=security_data.get('max_file_size_mb', self.security.max_file_size_mb),
                custom_patterns=security_data.get('custom_patterns', self.security.custom_patterns)
            )
        
        # Audit configuration
        if 'audit' in self.config_data:
            audit_data = self.config_data['audit']
            self.audit = AuditConfig(
                enabled=audit_data.get('enabled', self.audit.enabled),
                retention_days=audit_data.get('retention_days', self.audit.retention_days),
                log_format=audit_data.get('log_format', self.audit.log_format),
                include_content=audit_data.get('include_content', self.audit.include_content),
                compress_old_logs=audit_data.get('compress_old_logs', self.audit.compress_old_logs)
            )
        
        # Remediation configuration
        if 'remediation' in self.config_data:
            remediation_data = self.config_data['remediation']
            self.remediation = RemediationConfig(
                interactive_mode=remediation_data.get('interactive_mode', self.remediation.interactive_mode),
                create_backups=remediation_data.get('create_backups', self.remediation.create_backups),
                clean_git_history=remediation_data.get('clean_git_history', self.remediation.clean_git_history),
                update_gitignore=remediation_data.get('update_gitignore', self.remediation.update_gitignore),
                remove_files=remediation_data.get('remove_files', self.remediation.remove_files)
            )
        
        # Notification configuration
        if 'notification' in self.config_data:
            notification_data = self.config_data['notification']
            self.notification = NotificationConfig(
                slack_webhook=notification_data.get('slack_webhook'),
                email_alerts=notification_data.get('email_alerts', self.notification.email_alerts),
                console_notifications=notification_data.get('console_notifications', self.notification.console_notifications)
            )
        
        # Integration configuration
        if 'integration' in self.config_data:
            integration_data = self.config_data['integration']
            self.integration = IntegrationConfig(
                github_checks=integration_data.get('github_checks', self.integration.github_checks),
                jira_project=integration_data.get('jira_project'),
                ci_cd_integration=integration_data.get('ci_cd_integration', self.integration.ci_cd_integration)
            )
    
    def save_config(self, config_path: Optional[str] = None):
        """Save current configuration to file"""
        save_path = Path(config_path) if config_path else self.config_path
        
        if not save_path:
            save_path = Path.cwd() / ".gitguard.yaml"
        
        config_dict = {
            'security': asdict(self.security),
            'audit': asdict(self.audit),
            'remediation': asdict(self.remediation),
            'notification': asdict(self.notification),
            'integration': asdict(self.integration)
        }
        
        # Remove None values
        config_dict = self._remove_none_values(config_dict)
        
        try:
            with open(save_path, 'w') as f:
                if save_path.suffix.lower() in ['.yaml', '.yml']:
                    yaml.safe_dump(config_dict, f, default_flow_style=False, indent=2)
                elif save_path.suffix.lower() == '.json':
                    json.dump(config_dict, f, indent=2)
                else:
                    # Default to YAML
                    yaml.safe_dump(config_dict, f, default_flow_style=False, indent=2)
        
        except Exception as e:
            raise ConfigurationError(f"Failed to save config file: {str(e)}", str(save_path))
        
        self.config_path = save_path
    
    def _remove_none_values(self, data):
        """Recursively remove None values from dictionary"""
        if isinstance(data, dict):
            return {k: self._remove_none_values(v) for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [self._remove_none_values(item) for item in data if item is not None]
        else:
            return data
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration as dictionary"""
        return {
            'security': asdict(SecurityConfig()),
            'audit': asdict(AuditConfig()),
            'remediation': asdict(RemediationConfig()),
            'notification': asdict(NotificationConfig()),
            'integration': asdict(IntegrationConfig())
        }
    
    def validate(self):
        """Validate configuration settings"""
        errors = []
        
        # Validate security config
        if self.security.max_file_size_mb <= 0:
            errors.append("security.max_file_size_mb must be positive")
        
        if self.security.max_file_size_mb > 100:
            errors.append("security.max_file_size_mb should not exceed 100MB")
        
        # Validate audit config
        if self.audit.retention_days <= 0:
            errors.append("audit.retention_days must be positive")
        
        if self.audit.log_format not in ['json', 'yaml', 'text']:
            errors.append("audit.log_format must be 'json', 'yaml', or 'text'")
        
        # Validate notification config
        if self.notification.slack_webhook and not self.notification.slack_webhook.startswith('https://hooks.slack.com/'):
            errors.append("notification.slack_webhook must be a valid Slack webhook URL")
        
        if errors:
            raise ConfigurationError(f"Configuration validation failed: {', '.join(errors)}")
    
    def create_sample_config(self, output_path: str = ".gitguard.yaml"):
        """Create a sample configuration file"""
        sample_config = {
            'security': {
                'block_on_critical': True,
                'block_on_high': False,
                'auto_fix_enabled': True,
                'scan_file_contents': True,
                'max_file_size_mb': 1,
                'custom_patterns': [
                    'COMPANY_API_KEY_.*',
                    'INTERNAL_TOKEN_.*'
                ]
            },
            'audit': {
                'enabled': True,
                'retention_days': 90,
                'log_format': 'json',
                'include_content': False,
                'compress_old_logs': True
            },
            'remediation': {
                'interactive_mode': True,
                'create_backups': True,
                'clean_git_history': True,
                'update_gitignore': True,
                'remove_files': False
            },
            'notification': {
                'console_notifications': True,
                'email_alerts': False,
                'slack_webhook': None
            },
            'integration': {
                'github_checks': False,
                'jira_project': None,
                'ci_cd_integration': False
            }
        }
        
        try:
            with open(output_path, 'w') as f:
                yaml.safe_dump(sample_config, f, default_flow_style=False, indent=2)
            print(f"Sample configuration created: {output_path}")
        except Exception as e:
            raise ConfigurationError(f"Failed to create sample config: {str(e)}")

def load_config(config_path: Optional[str] = None) -> GitGuardConfig:
    """Convenience function to load GitGuard configuration"""
    return GitGuardConfig(config_path)