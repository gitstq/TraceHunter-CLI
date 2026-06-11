# Contributing to TraceHunter-CLI

Thank you for your interest in contributing to TraceHunter-CLI! This document provides guidelines for contributing.

## Code of Conduct

- Be respectful to all contributors
- Focus on constructive feedback
- Maintain professional communication

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Error logs if applicable

### Adding New Sites

1. Edit `tracehunter_cli/sites_db.py`
2. Add a new entry to the `SITES` list following the format:
```python
{
    "name": "sitename",
    "category": "social",  # social/tech/media/gaming/finance/education/forum/shopping/other
    "url": "https://example.com/{username}",
    "presence_strs": ["unique string when account exists"],
    "absence_strs": ["unique string when account doesn't exist"],
    "method": "html",  # html or json
    "tags": ["tag1", "tag2"],
}
```
3. Test the new site detection
4. Submit a pull request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/gitstq/TraceHunter-CLI.git
cd TraceHunter-CLI

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Run directly
python -m tracehunter_cli -u testuser
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit PR with clear description

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
