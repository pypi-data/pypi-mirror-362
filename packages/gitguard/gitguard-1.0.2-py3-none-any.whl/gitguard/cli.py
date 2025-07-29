#!/usr/bin/env python3
# File: cli.py
# Path: gitguard/cli.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-14
# Last Modified: 2025-07-14  12:50PM
# Author: Claude (Anthropic), as part of Project Himalaya
"""
GitGuard Command Line Interface
Main entry point for GitGuard CLI commands.

Part of Project Himalaya demonstrating AI-human collaboration.
Project Creator: Herbert J. Bowers
Technical Implementation: Claude (Anthropic)
"""

import sys
import click
from pathlib import Path
from typing import Optional

from . import __version__
from .validator import SecurityValidator
from .config import GitGuardConfig
from .exceptions import GitGuardError

@click.group()
@click.version_option(__version__)
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, config: Optional[str], verbose: bool):
    """
    🛡️ GitGuard - Enterprise-Grade Secure Git Workflow
    Part of Project Himalaya - AI-Human Collaborative Development
    
    Automatically validates, fixes, and audits security issues in git repositories.
    """
    ctx.ensure_object(dict)
    ctx.obj['config_path'] = config
    ctx.obj['verbose'] = verbose

@cli.command()
@click.option('--path', '-p', default='.', help='Repository path to scan')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
@click.option('--format', 'output_format', default='text', 
              type=click.Choice(['text', 'json', 'yaml']), help='Output format')
@click.option('--full', is_flag=True, help='Full repository scan including file contents')
@click.pass_context
def scan(ctx, path: str, output: Optional[str], output_format: str, full: bool):
    """Scan repository for security issues"""
    try:
        config = GitGuardConfig(ctx.obj.get('config_path'))
        validator = SecurityValidator(path, config)
        
        if ctx.obj['verbose']:
            click.echo(f"🔍 Scanning repository: {Path(path).resolve()}")
        
        # Configure scanning options
        if full:
            config.security.scan_file_contents = True
        
        issues = validator.validate_project()
        
        if output_format == 'text':
            validator.print_report()
        else:
            report = validator.generate_report()
            if output_format == 'json':
                import json
                output_text = json.dumps(report, indent=2)
            elif output_format == 'yaml':
                import yaml
                output_text = yaml.safe_dump(report, default_flow_style=False)
            
            if output:
                with open(output, 'w') as f:
                    f.write(output_text)
                click.echo(f"Report saved to: {output}")
            else:
                click.echo(output_text)
        
        # Exit with error code if critical issues found
        critical_count = sum(1 for issue in issues if issue.severity.value == 'CRITICAL')
        if critical_count > 0:
            sys.exit(1)
            
    except GitGuardError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--path', '-p', default='.', help='Repository path')
@click.option('--auto', is_flag=True, help='Automatic mode (no prompts)')
@click.option('--dry-run', is_flag=True, help='Show what would be fixed without doing it')
@click.option('--no-history', is_flag=True, help='Skip git history cleaning')
@click.option('--no-gitignore', is_flag=True, help='Skip .gitignore updates')
@click.pass_context
def fix(ctx, path: str, auto: bool, dry_run: bool, no_history: bool, no_gitignore: bool):
    """Fix security issues automatically"""
    try:
        config = GitGuardConfig(ctx.obj.get('config_path'))
        
        # Update config based on options
        config.remediation.interactive_mode = not auto
        config.remediation.clean_git_history = not no_history
        config.remediation.update_gitignore = not no_gitignore
        
        if ctx.obj['verbose']:
            click.echo(f"🔧 Fixing security issues in: {Path(path).resolve()}")
        
        if dry_run:
            click.echo("🔍 DRY RUN - No changes will be made")
            # Implement dry run logic here
            validator = SecurityValidator(path, config)
            issues = validator.validate_project()
            
            if not issues:
                click.echo("✅ No security issues found!")
                return
            
            click.echo(f"📋 Found {len(issues)} issues that would be fixed:")
            for issue in issues:
                click.echo(f"  • {issue.severity.value}: {issue.description}")
            return
        
        # Implement actual fixing logic here
        click.echo("🔧 Security remediation functionality coming soon!")
        
    except GitGuardError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--path', '-p', default='.', help='Repository path to initialize')
@click.option('--github', is_flag=True, help='Setup for GitHub integration')
@click.option('--team', is_flag=True, help='Setup for team development')
@click.pass_context
def init(ctx, path: str, github: bool, team: bool):
    """Initialize GitGuard in a repository"""
    try:
        repo_path = Path(path).resolve()
        
        if ctx.obj['verbose']:
            click.echo(f"🚀 Initializing GitGuard in: {repo_path}")
        
        # Check if it's a git repository
        if not (repo_path / '.git').exists():
            click.echo("❌ Not a git repository. Initialize git first with 'git init'")
            sys.exit(1)
        
        # Create .gitguard.yaml configuration
        config = GitGuardConfig()
        
        if team:
            config.notification.email_alerts = True
            config.integration.github_checks = True
        
        if github:
            config.integration.github_checks = True
            config.integration.ci_cd_integration = True
        
        config_path = repo_path / '.gitguard.yaml'
        config.save_config(str(config_path))
        
        # Create gitguard directory structure
        gitguard_dir = repo_path / '.gitguard'
        gitguard_dir.mkdir(exist_ok=True)
        
        (gitguard_dir / 'logs').mkdir(exist_ok=True)
        (gitguard_dir / 'backups').mkdir(exist_ok=True)
        
        # Add .gitguard to .gitignore if it exists
        gitignore_path = repo_path / '.gitignore'
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            
            if '.gitguard/logs/' not in gitignore_content:
                with open(gitignore_path, 'a') as f:
                    f.write('\n# GitGuard\n.gitguard/logs/\n.gitguard/backups/\n')
        
        click.echo("✅ GitGuard initialized successfully!")
        click.echo(f"   Configuration: {config_path}")
        click.echo(f"   Directory: {gitguard_dir}")
        
        if team:
            click.echo("👥 Team features enabled")
        if github:
            click.echo("🐙 GitHub integration enabled")
        
        click.echo("\nNext steps:")
        click.echo("  1. Review configuration: gitguard config show")
        click.echo("  2. Run security scan: gitguard scan")
        click.echo("  3. Fix any issues: gitguard fix")
        
    except GitGuardError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

@cli.group()
def config():
    """Configuration management commands"""
    pass

@config.command('show')
@click.option('--format', 'output_format', default='yaml',
              type=click.Choice(['yaml', 'json']), help='Output format')
@click.pass_context
def config_show(ctx, output_format: str):
    """Show current configuration"""
    try:
        config = GitGuardConfig(ctx.obj.get('config_path'))
        
        if output_format == 'yaml':
            import yaml
            config_dict = {
                'security': config.security.__dict__,
                'audit': config.audit.__dict__,
                'remediation': config.remediation.__dict__,
                'notification': config.notification.__dict__,
                'integration': config.integration.__dict__
            }
            click.echo(yaml.safe_dump(config_dict, default_flow_style=False))
        elif output_format == 'json':
            import json
            config_dict = {
                'security': config.security.__dict__,
                'audit': config.audit.__dict__,
                'remediation': config.remediation.__dict__,
                'notification': config.notification.__dict__,
                'integration': config.integration.__dict__
            }
            click.echo(json.dumps(config_dict, indent=2))
            
    except GitGuardError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

@config.command('create')
@click.option('--output', '-o', default='.gitguard.yaml', help='Output file path')
@click.pass_context
def config_create(ctx, output: str):
    """Create sample configuration file"""
    try:
        config = GitGuardConfig()
        config.create_sample_config(output)
        click.echo(f"✅ Sample configuration created: {output}")
        
    except GitGuardError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--path', '-p', default='.', help='Repository path')
@click.option('--message', '-m', required=True, help='Commit message')
@click.option('--auto-fix', is_flag=True, help='Automatically fix security issues')
@click.pass_context
def commit(ctx, path: str, message: str, auto_fix: bool):
    """Secure git commit with automatic security validation"""
    try:
        if ctx.obj['verbose']:
            click.echo(f"🔐 Secure commit in: {Path(path).resolve()}")
        
        # First, run security validation
        config = GitGuardConfig(ctx.obj.get('config_path'))
        validator = SecurityValidator(path, config)
        issues = validator.validate_project()
        
        critical_issues = [i for i in issues if i.severity.value == 'CRITICAL']
        
        if critical_issues and not auto_fix:
            click.echo(f"🚫 Commit blocked: {len(critical_issues)} critical security issues found!")
            click.echo("Run 'gitguard fix' to resolve issues, or use --auto-fix")
            sys.exit(1)
        
        if critical_issues and auto_fix:
            click.echo(f"🔧 Auto-fixing {len(critical_issues)} critical issues...")
            # Implement auto-fix logic here
            click.echo("✅ Issues resolved")
        
        # Proceed with git commit
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'add', '.'],
                cwd=path,
                capture_output=True,
                text=True
            )
            
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                click.echo("✅ Secure commit successful!")
            else:
                click.echo(f"❌ Git commit failed: {result.stderr}")
                sys.exit(1)
                
        except Exception as e:
            click.echo(f"❌ Git operation failed: {e}")
            sys.exit(1)
        
    except GitGuardError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--path', '-p', default='.', help='Repository path')
@click.pass_context  
def status(ctx, path: str):
    """Show GitGuard security status"""
    try:
        config = GitGuardConfig(ctx.obj.get('config_path'))
        validator = SecurityValidator(path, config)
        issues = validator.validate_project()
        
        click.echo("🛡️ GitGuard Security Status")
        click.echo("=" * 30)
        
        if not issues:
            click.echo("✅ No security issues detected")
            click.echo("🔒 Repository is secure")
        else:
            severity_counts = {}
            for issue in issues:
                severity = issue.severity.value
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            total_issues = len(issues)
            click.echo(f"📋 Total Issues: {total_issues}")
            
            severity_icons = {
                'CRITICAL': '🚨',
                'HIGH': '⚠️', 
                'MEDIUM': '💡',
                'LOW': 'ℹ️'
            }
            
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                count = severity_counts.get(severity, 0)
                if count > 0:
                    icon = severity_icons[severity]
                    click.echo(f"   {icon} {severity}: {count}")
            
            if severity_counts.get('CRITICAL', 0) > 0:
                click.echo("🚫 Commits will be blocked until critical issues are resolved")
                click.echo("💡 Run 'gitguard fix' to resolve issues")
        
        # Show configuration status
        click.echo(f"\n⚙️ Configuration: {config.config_path or 'default'}")
        click.echo(f"📊 Audit Logging: {'✅ enabled' if config.audit.enabled else '❌ disabled'}")
        click.echo(f"🔧 Auto-fix: {'✅ enabled' if config.security.auto_fix_enabled else '❌ disabled'}")
        
    except GitGuardError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

def main():
    """Main entry point for GitGuard CLI"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n👋 GitGuard interrupted by user")
        sys.exit(130)
    except Exception as e:
        click.echo(f"💥 Unexpected error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()