# File: validator.py
# Path: gitguard/validator.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-14
# Last Modified: 2025-07-14  12:45PM
# Author: Claude (Anthropic), as part of Project Himalaya
"""
Security Validator - Core security validation engine for GitGuard
Detects sensitive data exposure, git tracking issues, and policy violations.

Part of Project Himalaya demonstrating AI-human collaboration.
Project Creator: Herbert J. Bowers
Technical Implementation: Claude (Anthropic)
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from .exceptions import SecurityValidationError
from .config import GitGuardConfig

class SecurityLevel(Enum):
    """Security issue severity levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IssueCategory(Enum):
    """Categories of security issues"""
    EXPOSED_CREDENTIALS = "EXPOSED_CREDENTIALS"
    OVERLY_BROAD = "OVERLY_BROAD"
    MISSING_PROTECTION = "MISSING_PROTECTION"
    POLICY_VIOLATION = "POLICY_VIOLATION"

@dataclass
class SecurityIssue:
    """Represents a security issue found during validation"""
    severity: SecurityLevel
    category: IssueCategory
    description: str
    file_path: str
    line_number: Optional[int] = None
    recommendation: str = ""
    pattern_matched: str = ""
    confidence: float = 1.0

class SecurityValidator:
    """Core security validation engine"""
    
    def __init__(self, project_path: str = ".", config: Optional[GitGuardConfig] = None):
        self.project_path = Path(project_path).resolve()
        self.config = config or GitGuardConfig()
        self.issues: List[SecurityIssue] = []
        
        # Load security patterns
        self._load_patterns()
    
    def _load_patterns(self):
        """Load security detection patterns"""
        # Dangerous .gitignore patterns
        self.dangerous_patterns = [
            r'^\*\.json$',
            r'^\*\.js$', 
            r'^\*\.py$',
            r'^\*\.env$',
            r'^\*\.key$',
            r'^\*\.pem$',
            r'^\*\.p12$',
            r'^\*\.pfx$'
        ]
        
        # Sensitive file patterns (high confidence)
        self.sensitive_patterns = [
            # Credentials and secrets
            r'.*credential.*',
            r'.*secret.*',
            r'.*password.*',
            r'.*passwd.*',
            r'.*token.*',
            r'.*key.*',
            r'.*auth.*',
            
            # API and service specific
            r'.*api.*key.*',
            r'.*access.*key.*',
            r'.*service.*account.*',
            r'.*private.*key.*',
            
            # File extensions
            r'.*\.pem$',
            r'.*\.p12$', 
            r'.*\.pfx$',
            r'.*\.key$',
            r'.*\.crt$',
            r'.*\.cer$',
            
            # Environment and config
            r'.*\.env$',
            r'.*\.env\..*',
            r'.*config.*\.json$',
            r'.*settings.*\.json$',
            r'.*secrets.*\.json$',
            
            # Database
            r'.*database.*',
            r'.*db.*config.*',
            r'.*connection.*string.*',
            
            # Cloud providers
            r'.*aws.*credential.*',
            r'.*gcp.*credential.*', 
            r'.*azure.*credential.*',
            r'.*google.*credential.*',
        ]
        
        # Content patterns (for scanning file contents)
        self.content_patterns = [
            # AWS
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
            (r'[0-9a-zA-Z/+]{40}', 'AWS Secret Access Key'),
            
            # Google API
            (r'AIza[0-9A-Za-z\\-_]{35}', 'Google API Key'),
            (r'"type":\s*"service_account"', 'Google Service Account'),
            
            # GitHub
            (r'ghp_[0-9a-zA-Z]{36}', 'GitHub Personal Access Token'),
            (r'ghs_[0-9a-zA-Z]{36}', 'GitHub App Secret'),
            
            # Generic patterns
            (r'password\s*[:=]\s*["\'][^"\']{8,}["\']', 'Password in config'),
            (r'api[_-]?key\s*[:=]\s*["\'][^"\']{20,}["\']', 'API Key in config'),
            (r'secret\s*[:=]\s*["\'][^"\']{16,}["\']', 'Secret in config'),
            
            # Database connections
            (r'mongodb://[^\\s]+', 'MongoDB Connection String'),
            (r'mysql://[^\\s]+', 'MySQL Connection String'),
            (r'postgresql://[^\\s]+', 'PostgreSQL Connection String'),
            
            # JWT tokens
            (r'eyJ[A-Za-z0-9_/+-]*\.eyJ[A-Za-z0-9_/+-]*\.[A-Za-z0-9_/+-]*', 'JWT Token'),
        ]
    
    def validate_project(self) -> List[SecurityIssue]:
        """Main validation method - returns list of security issues"""
        self.issues = []
        
        # Check if it's a git repository
        if not self._is_git_repository():
            self.issues.append(SecurityIssue(
                severity=SecurityLevel.LOW,
                category=IssueCategory.MISSING_PROTECTION,
                description="Directory is not a git repository",
                file_path=str(self.project_path),
                recommendation="Initialize git repository if needed"
            ))
            return self.issues
        
        # Validate .gitignore
        self._validate_gitignore()
        
        # Check for exposed sensitive files
        self._check_exposed_sensitive_files()
        
        # Check git history for sensitive files
        self._check_git_history()
        
        # Check for sensitive files in working directory
        self._check_working_directory()
        
        # Scan file contents for secrets
        self._scan_file_contents()
        
        return self.issues
    
    def _is_git_repository(self) -> bool:
        """Check if directory is a git repository"""
        return (self.project_path / '.git').exists()
    
    def _validate_gitignore(self):
        """Validate .gitignore file for security issues"""
        gitignore_path = self.project_path / '.gitignore'
        
        if not gitignore_path.exists():
            self.issues.append(SecurityIssue(
                severity=SecurityLevel.MEDIUM,
                category=IssueCategory.MISSING_PROTECTION,
                description="No .gitignore file found",
                file_path=str(gitignore_path),
                recommendation="Create .gitignore file with appropriate exclusions"
            ))
            return
        
        # Read and analyze .gitignore
        try:
            with open(gitignore_path, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            self.issues.append(SecurityIssue(
                severity=SecurityLevel.LOW,
                category=IssueCategory.MISSING_PROTECTION,
                description=f"Could not read .gitignore file: {str(e)}",
                file_path=str(gitignore_path),
                recommendation="Check .gitignore file permissions"
            ))
            return
        
        for line_num, line in enumerate(lines, 1):
            clean_line = line.strip()
            if not clean_line or clean_line.startswith('#'):
                continue
                
            # Check for dangerous patterns
            for pattern in self.dangerous_patterns:
                if re.match(pattern, clean_line):
                    self.issues.append(SecurityIssue(
                        severity=SecurityLevel.HIGH,
                        category=IssueCategory.OVERLY_BROAD,
                        description=f"Overly broad pattern '{clean_line}' may exclude important files",
                        file_path=str(gitignore_path),
                        line_number=line_num,
                        recommendation=f"Replace '{clean_line}' with specific file patterns",
                        pattern_matched=pattern
                    ))
    
    def _check_exposed_sensitive_files(self):
        """Check for sensitive files currently tracked in git"""
        try:
            result = subprocess.run(
                ['git', 'ls-files'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                tracked_files = result.stdout.splitlines()
                
                for file_path in tracked_files:
                    for pattern in self.sensitive_patterns:
                        if re.search(pattern, file_path, re.IGNORECASE):
                            self.issues.append(SecurityIssue(
                                severity=SecurityLevel.CRITICAL,
                                category=IssueCategory.EXPOSED_CREDENTIALS,
                                description=f"Sensitive file '{file_path}' is tracked in git",
                                file_path=file_path,
                                recommendation=f"Remove with: git rm --cached {file_path}",
                                pattern_matched=pattern
                            ))
                            break
        except Exception as e:
            self.issues.append(SecurityIssue(
                severity=SecurityLevel.LOW,
                category=IssueCategory.MISSING_PROTECTION,
                description=f"Could not check git tracked files: {str(e)}",
                file_path=str(self.project_path),
                recommendation="Manually verify tracked files"
            ))
    
    def _check_git_history(self):
        """Check git history for sensitive files"""
        try:
            result = subprocess.run(
                ['git', 'log', '--all', '--full-history', '--name-only', '--pretty=format:'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                history_files = set(result.stdout.splitlines())
                history_files.discard('')  # Remove empty strings
                
                for file_path in history_files:
                    for pattern in self.sensitive_patterns:
                        if re.search(pattern, file_path, re.IGNORECASE):
                            # Check if file is currently tracked
                            if not self._is_file_currently_tracked(file_path):
                                self.issues.append(SecurityIssue(
                                    severity=SecurityLevel.CRITICAL,
                                    category=IssueCategory.EXPOSED_CREDENTIALS,
                                    description=f"Sensitive file '{file_path}' exists in git history but not in current commit",
                                    file_path=file_path,
                                    recommendation="Remove from history with git filter-branch or BFG Repo-Cleaner",
                                    pattern_matched=pattern
                                ))
                            break
        except Exception as e:
            self.issues.append(SecurityIssue(
                severity=SecurityLevel.LOW,
                category=IssueCategory.MISSING_PROTECTION,
                description=f"Could not check git history: {str(e)}",
                file_path=str(self.project_path),
                recommendation="Manually verify git history for sensitive files"
            ))
    
    def _is_file_currently_tracked(self, file_path: str) -> bool:
        """Check if file is currently tracked in git"""
        try:
            result = subprocess.run(
                ['git', 'ls-files', '--error-unmatch', file_path],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def _check_working_directory(self):
        """Check for sensitive files in working directory"""
        for root, dirs, files in os.walk(self.project_path):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')
                
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.project_path)
                
                for pattern in self.sensitive_patterns:
                    if re.search(pattern, file, re.IGNORECASE):
                        # Check if file is properly ignored
                        if not self._is_file_ignored(relative_path):
                            self.issues.append(SecurityIssue(
                                severity=SecurityLevel.HIGH,
                                category=IssueCategory.MISSING_PROTECTION,
                                description=f"Sensitive file '{relative_path}' is not ignored",
                                file_path=relative_path,
                                recommendation=f"Add '{relative_path}' to .gitignore",
                                pattern_matched=pattern
                            ))
                        break
    
    def _is_file_ignored(self, file_path: str) -> bool:
        """Check if file is ignored by git"""
        try:
            result = subprocess.run(
                ['git', 'check-ignore', file_path],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def _scan_file_contents(self):
        """Scan file contents for embedded secrets"""
        # Only scan text files under a reasonable size
        max_file_size = 1024 * 1024  # 1MB
        text_extensions = {'.py', '.js', '.json', '.yaml', '.yml', '.txt', '.md', '.env', '.conf', '.cfg'}
        
        for root, dirs, files in os.walk(self.project_path):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')
            
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_path)
                
                # Skip non-text files and large files
                if file_path.suffix.lower() not in text_extensions:
                    continue
                    
                try:
                    if file_path.stat().st_size > max_file_size:
                        continue
                        
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # Scan content for secret patterns
                    for pattern, description in self.content_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            # Calculate line number
                            line_num = content[:match.start()].count('\n') + 1
                            
                            self.issues.append(SecurityIssue(
                                severity=SecurityLevel.CRITICAL,
                                category=IssueCategory.EXPOSED_CREDENTIALS,
                                description=f"{description} detected in file content",
                                file_path=str(relative_path),
                                line_number=line_num,
                                recommendation="Remove sensitive data and use environment variables or secure config",
                                pattern_matched=pattern,
                                confidence=0.9  # High confidence for content matches
                            ))
                            
                except Exception:
                    # Skip files that can't be read
                    continue
    
    def generate_report(self) -> Dict:
        """Generate comprehensive security report"""
        severity_counts = {
            SecurityLevel.CRITICAL: 0,
            SecurityLevel.HIGH: 0, 
            SecurityLevel.MEDIUM: 0,
            SecurityLevel.LOW: 0
        }
        
        category_counts = {}
        
        for issue in self.issues:
            severity_counts[issue.severity] += 1
            category_counts[issue.category] = category_counts.get(issue.category, 0) + 1
        
        return {
            'project_path': str(self.project_path),
            'total_issues': len(self.issues),
            'severity_counts': {k.value: v for k, v in severity_counts.items()},
            'category_counts': {k.value: v for k, v in category_counts.items()},
            'issues': [
                {
                    'severity': issue.severity.value,
                    'category': issue.category.value,
                    'description': issue.description,
                    'file_path': issue.file_path,
                    'line_number': issue.line_number,
                    'recommendation': issue.recommendation,
                    'pattern_matched': issue.pattern_matched,
                    'confidence': issue.confidence
                }
                for issue in self.issues
            ]
        }
    
    def print_report(self):
        """Print formatted security report"""
        report = self.generate_report()
        
        print("=" * 60)
        print("🔒 GITGUARD SECURITY VALIDATION REPORT")
        print("=" * 60)
        print(f"Project: {report['project_path']}")
        print(f"Total Issues: {report['total_issues']}")
        print()
        
        # Print severity summary
        print("SEVERITY BREAKDOWN:")
        severity_icons = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '💡', 
            'LOW': 'ℹ️'
        }
        
        for severity, count in report['severity_counts'].items():
            if count > 0:
                icon = severity_icons.get(severity, '•')
                print(f"  {icon} {severity}: {count}")
        print()
        
        # Print issues by severity
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            severity_issues = [i for i in self.issues if i.severity.value == severity]
            if severity_issues:
                print(f"{severity} ISSUES:")
                for issue in severity_issues:
                    print(f"  • {issue.description}")
                    print(f"    File: {issue.file_path}")
                    if issue.line_number:
                        print(f"    Line: {issue.line_number}")
                    if issue.recommendation:
                        print(f"    Fix: {issue.recommendation}")
                    print()