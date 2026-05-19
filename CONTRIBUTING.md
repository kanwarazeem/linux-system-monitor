# Contributing to Linux System Monitor

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- pip/poetry

### Development Setup

```bash
# Clone the repository
git clone https://github.com/kanwarazeem/linux-system-monitor.git
cd linux-system-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow PEP 8 style guide
- Add docstrings to functions
- Update type hints
- Write tests for new code

### 3. Code Quality

```bash
# Run linting
flake8 src/ tests/

# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Security checks
bandit -r src/
```

### 4. Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_cpu.py

# Run with verbose output
pytest -v tests/
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub.

## Code Style Guide

### Python Style
- Follow PEP 8
- Line length: 100 characters
- Use type hints
- Write docstrings (Google style)

### Example Function

```python
def calculate_cpu_percentage(usage: float, threshold: float) -> bool:
    """
    Calculate if CPU usage exceeds threshold.
    
    Args:
        usage: Current CPU usage percentage
        threshold: Alert threshold percentage
        
    Returns:
        True if usage exceeds threshold, False otherwise
        
    Example:
        >>> calculate_cpu_percentage(85.5, 80.0)
        True
    """
    return usage > threshold
```

### Example Class

```python
class CPUMonitor:
    """Monitor CPU usage and statistics."""
    
    def __init__(self, interval: int = 1):
        """
        Initialize CPU monitor.
        
        Args:
            interval: Sampling interval in seconds
        """
        self.interval = interval
    
    def get_usage(self) -> float:
        """Get current CPU usage percentage."""
        pass
```

## Testing Guidelines

### Test File Structure

```python
import pytest
from src.cpu_monitor import CPUMonitor

class TestCPUMonitor:
    """Tests for CPU monitoring."""
    
    @pytest.fixture
    def monitor(self):
        """Fixture providing CPU monitor instance."""
        return CPUMonitor(interval=1)
    
    def test_initialization(self, monitor):
        """Test monitor initialization."""
        assert monitor.interval == 1
    
    @patch('psutil.cpu_percent')
    def test_get_usage(self, mock_cpu, monitor):
        """Test getting CPU usage."""
        mock_cpu.return_value = 45.5
        usage = monitor.get_usage()
        assert usage == 45.5
```

### Test Coverage Goals
- Overall: > 80%
- Critical functions: 100%
- New features: Must have tests

## Documentation

### Docstring Format (Google Style)

```python
def function(arg1: str, arg2: int) -> dict:
    """
    Brief description.
    
    Longer description if needed. Can span multiple
    lines to explain complex behavior.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
        
    Example:
        >>> function("test", 42)
        {'key': 'value'}
    """
    pass
```

### README Updates
- Document new features
- Add usage examples
- Update screenshots if UI changed
- Add troubleshooting steps

## Commit Message Format

Follow conventional commits:

```
type(scope): subject

body

footer
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Code style (no logic change)
- **refactor**: Code refactoring
- **perf**: Performance improvement
- **test**: Add/update tests
- **chore**: Maintenance

### Examples

```
feat(cpu-monitor): add per-core statistics

Add support for displaying per-core CPU usage
statistics in the monitoring output.

Fixes #123
```

```
fix(memory-monitor): correct swap usage calculation

The swap usage calculation was using physical
memory instead of swap memory. This commit fixes
the issue.
```

## Pull Request Process

1. **Before submitting:**
   - Run all tests: `pytest`
   - Check code quality: `flake8 src/ tests/`
   - Verify coverage: `pytest --cov=src`

2. **PR Description should include:**
   - What problem does it solve?
   - How does it solve it?
   - Any breaking changes?
   - Related issues/PRs

3. **PR Template:**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change

## Testing
Describe tests added/modified

## Checklist
- [ ] Tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No new warnings generated
```

4. **Review process:**
   - At least 1 approval required
   - CI/CD must pass
   - No conflicts with main branch

## Issue Reporting

### Bug Report Template

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Ubuntu 22.04
- Python: 3.10
- Version: 1.0.0

## Logs
```
error message here
```
```

### Feature Request Template

```markdown
## Description
What feature would you like?

## Use Case
Why do you need this feature?

## Proposed Solution
How would you implement it?

## Alternatives Considered
Other approaches?
```

## Code Review Checklist

Reviewers should check:

- [ ] Code follows style guide
- [ ] Functions have docstrings
- [ ] Type hints present
- [ ] Tests added for new code
- [ ] Tests pass
- [ ] No breaking changes
- [ ] Documentation updated
- [ ] No security issues
- [ ] No performance regression

## Release Process

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions will create release

## Questions?

- Check existing issues/discussions
- Read documentation in docs/
- Open a discussion on GitHub

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
