# Basic GitGuard Example

<img src="../../Project_Himalaya_Icon_Round_256.png" alt="Project Himalaya" width="32" height="32" style="vertical-align: middle;"> *Part of Project Himalaya*

This example demonstrates basic GitGuard usage for individual developers.

## Quick Start

1. **Install GitGuard**:
   ```bash
   pip install gitguard
   ```

2. **Initialize in your repository**:
   ```bash
   cd your-project
   gitguard init
   ```

3. **Scan for security issues**:
   ```bash
   gitguard scan
   ```

4. **Fix issues automatically**:
   ```bash
   gitguard fix --auto
   ```

5. **Use secure commit workflow**:
   ```bash
   gitguard commit -m "Add new feature"
   ```

## Configuration

The basic configuration file (`.gitguard.yaml`) provides sensible defaults:

```yaml
security:
  block_on_critical: true
  block_on_high: false
  auto_fix_enabled: true

audit:
  enabled: true
  retention_days: 30

remediation:
  interactive_mode: true
  create_backups: true
```

## Common Workflow

### Daily Development
```bash
# Start working
gitguard status

# Make changes to your code
# ...

# Secure commit (automatically validates)
gitguard commit -m "Add user authentication"

# If issues are found
gitguard fix

# Push changes
git push
```

### Weekly Security Review
```bash
# Full security scan
gitguard scan --full

# Generate security report
gitguard scan --output security-report.json --format json

# Review and fix any issues
gitguard fix --dry-run  # Preview first
gitguard fix --auto     # Apply fixes
```

## What GitGuard Protects Against

### Automatically Detected
- ✅ API keys and secrets in code
- ✅ Database passwords and connection strings
- ✅ SSL certificates and private keys
- ✅ Environment variables in wrong locations
- ✅ Overly broad .gitignore patterns

### Example Detection
```python
# This would be flagged:
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "super-secret-password"

# This is better:
API_KEY = os.environ.get('API_KEY')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
```

## File Structure

```
your-project/
├── .gitguard.yaml          # GitGuard configuration
├── .gitguard/              # GitGuard data directory
│   ├── logs/              # Audit logs
│   └── backups/           # Automatic backups
├── .gitignore             # Updated by GitGuard
└── [your project files]
```

## Troubleshooting

### "No security issues found"
✅ Great! Your repository is secure.

### "Critical issues found"
🚨 Run `gitguard fix --auto` to resolve automatically.

### "Git history contains sensitive data"
🧹 Run `gitguard fix --auto` to clean history (creates backup first).

### "Permission denied"
🔑 Ensure you have write access to the repository.

## Next Steps

- **Team Setup**: See `../enterprise/` example for team configurations
- **CI/CD Integration**: See `../cicd/` example for automated checks
- **Custom Rules**: Edit `.gitguard.yaml` to add custom patterns