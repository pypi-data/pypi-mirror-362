![Project Himalaya](./Project_Himalaya_Banner.png)

# Contributing to GitGuard

*Part of Project Himalaya - AI-Human Collaborative Development Framework*

Thank you for your interest in contributing to GitGuard! This document provides guidelines and information for contributors.

## 🏔️ Project Himalaya Context

GitGuard is part of Project Himalaya, demonstrating optimal AI-human collaboration. All contributions should respect this collaborative model:

- **Human Contributors**: Provide vision, requirements, review, and strategic direction
- **AI Implementation**: Technical implementation, documentation, and testing (when applicable)
- **Transparent Attribution**: All contributions are clearly attributed to maintain project integrity

## 🎯 How to Contribute

### 🐛 Bug Reports

- **Search existing issues** before creating a new one
- **Use the bug report template** 
- **Provide detailed information**: OS, Python version, GitGuard version
- **Include reproduction steps** and expected vs actual behavior
- **Add relevant logs** from `.gitguard/logs/`

### 💡 Feature Requests

- **Check existing feature requests** first
- **Explain the use case** and why it's valuable
- **Provide examples** of how it would work
- **Consider backwards compatibility**

### 🔧 Code Contributions

#### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/gitguard.git
cd gitguard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

#### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gitguard

# Run specific test file
pytest tests/test_validator.py

# Run with verbose output
pytest -v
```

#### Code Standards

- **Python 3.8+** compatibility required
- **PEP 8** code style (enforced by black and flake8)
- **Type hints** for all public functions
- **Docstrings** for all public classes and methods
- **Comprehensive tests** for new features

#### Pull Request Process

1. **Create a feature branch** from main
2. **Make your changes** with appropriate tests
3. **Ensure all tests pass** locally
4. **Update documentation** if needed
5. **Submit a pull request** with clear description

## 🏗️ Project Structure

```
gitguard/
├── gitguard/                # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command line interface
│   ├── validator.py        # Security validation engine
│   ├── remediator.py       # Automatic remediation (contribute here!)
│   ├── auditor.py          # Audit logging (contribute here!)
│   ├── config.py           # Configuration management
│   └── exceptions.py       # Custom exceptions
├── tests/                  # Test suite
│   ├── test_validator.py   # Validator tests
│   ├── test_cli.py         # CLI tests (contribute here!)
│   └── test_config.py      # Config tests (contribute here!)
├── examples/               # Usage examples
├── docs/                   # Documentation
└── scripts/               # Utility scripts
```

## 🎨 Areas Needing Contributions

### High Priority

- **Remediator Implementation**: Automatic fixing of security issues
- **Auditor Implementation**: Comprehensive audit logging
- **CLI Commands**: Additional commands and options
- **Test Coverage**: More comprehensive test cases
- **Documentation**: User guides and API documentation

### Medium Priority

- **IDE Integrations**: VS Code, IntelliJ plugins
- **CI/CD Templates**: GitHub Actions, Jenkins, GitLab CI
- **Custom Patterns**: More security detection patterns
- **Performance**: Optimization for large repositories

### Future Features

- **Web Dashboard**: Security metrics visualization
- **Team Management**: Multi-user configurations
- **Cloud Integrations**: AWS, Azure, GCP secret detection
- **Machine Learning**: AI-powered threat detection

## 📝 Coding Guidelines

### Python Style

```python
# Good: Clear function with type hints and docstring
def validate_file(file_path: str, patterns: List[str]) -> List[SecurityIssue]:
    """
    Validate a file against security patterns.

    Args:
        file_path: Path to file to validate
        patterns: List of regex patterns to check

    Returns:
        List of security issues found

    Raises:
        SecurityValidationError: If validation fails
    """
    issues = []
    # Implementation here
    return issues

# Bad: No type hints, unclear naming
def check(f, p):
    stuff = []
    # Implementation here
    return stuff
```

### Error Handling

```python
# Good: Specific exceptions with context
try:
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
except subprocess.TimeoutExpired:
    raise SecurityValidationError(f"Command timed out: {command}")
except Exception as e:
    raise SecurityValidationError(f"Command failed: {command}, Error: {e}")

# Bad: Generic exception handling
try:
    result = subprocess.run(command)
except:
    pass
```

### Security Patterns

```python
# Good: Comprehensive pattern with context
PATTERNS = [
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID', 0.95),
    (r'[0-9a-zA-Z/+]{40}', 'AWS Secret Access Key', 0.8),
]

# Bad: Vague pattern without context
PATTERNS = [
    r'key.*secret',
]
```

## 🧪 Testing Guidelines

### Test Structure

```python
class TestSecurityValidator:
    def setup_method(self):
        """Setup test environment"""
        # Create temporary directory, mock objects, etc.

    def test_specific_functionality(self):
        """Test description explaining what this validates"""
        # Arrange
        # Act  
        # Assert

    def teardown_method(self):
        """Cleanup test environment"""
        # Remove temporary files, reset state, etc.
```

### Test Categories

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **CLI Tests**: Test command line interface
- **End-to-End Tests**: Test complete workflows

### Mocking Guidelines

```python
# Good: Mock external dependencies
@patch('subprocess.run')
def test_git_operation(self, mock_subprocess):
    mock_subprocess.return_value.returncode = 0
    mock_subprocess.return_value.stdout = "expected output"

    result = git_operation()
    assert result is True

# Bad: Don't mock internal logic being tested
@patch('gitguard.validator.SecurityValidator.validate_project')
def test_validation(self, mock_validate):
    # This doesn't actually test the validation logic
```

## 📚 Documentation

### Docstring Format

```python
def complex_function(param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """
    Brief description of what the function does.

    Longer description if needed, explaining the purpose,
    algorithm, or important implementation details.

    Args:
        param1: Description of first parameter
        param2: Description of optional parameter

    Returns:
        Dictionary containing results with keys:
        - 'status': Operation status
        - 'data': Result data

    Raises:
        ValueError: If param1 is empty
        SecurityValidationError: If validation fails

    Example:
        >>> result = complex_function("test", 42)
        >>> result['status']
        'success'
    """
```

### README Updates

- **Keep examples current** with latest API
- **Update feature lists** when adding capabilities
- **Maintain installation instructions**
- **Update compatibility information**

## 🚀 Release Process

### Version Numbering

- **Major (X.0.0)**: Breaking changes
- **Minor (1.X.0)**: New features, backwards compatible
- **Patch (1.0.X)**: Bug fixes, backwards compatible

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] CHANGELOG.md updated
- [ ] Security patterns updated if needed
- [ ] Example configurations reviewed

## 🏆 Recognition

Contributors will be:

- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes** for significant contributions
- **Invited to team discussions** for major contributors
- **Credited in documentation** for their specific contributions

## 📞 Getting Help

- **Discord**: Join our [community chat](https://discord.gg/gitguard)
- **GitHub Discussions**: Ask questions and share ideas
- **Email**: Contact maintainers at contribute@gitguard.dev
- **Office Hours**: Weekly contributor meetups (schedule TBD)

## 🎉 Thank You

Every contribution makes GitGuard better for the entire development community. Whether you're fixing a typo, adding a feature, or helping with documentation, your efforts are appreciated!

---

*By contributing to GitGuard, you agree that your contributions will be licensed under the MIT License.*