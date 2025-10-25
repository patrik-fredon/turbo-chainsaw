# Contributing to Fredon Menu

Thank you for your interest in contributing to Fredon Menu! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating a new issue, please:

1. **Search existing issues** to avoid duplicates
2. **Check the troubleshooting section** in the documentation
3. **Use the issue templates** when available

When creating an issue, include:
- Clear description of the problem
- Steps to reproduce
- System information (OS, Hyprland version, GTK version)
- Expected vs actual behavior
- Screenshots if applicable

### Bug Reports

- Use the `Bug Report` issue template
- Provide minimal reproduction case
- Include configuration file (redacted if needed)
- Attach log files if available

### Feature Requests

- Use the `Feature Request` issue template
- Describe the use case clearly
- Explain why this feature would be valuable
- Suggest implementation approach if you have ideas

## 🔧 Development Setup

### Prerequisites

- Arch Linux or similar Linux distribution
- Python 3.11+
- GTK3 development libraries
- Git
- Basic knowledge of Python and GTK

### Setting Up Development Environment

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/patrik-fredon/fredon-menu.git
   cd fredon-menu
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Development Dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run Tests**:
   ```bash
   python tests/run_tests.py
   ```

5. **Run Application**:
   ```bash
   python src/main.py --debug
   ```

### Code Style

- Follow [PEP 8](https://pep8.org/) guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [type hints](https://docs.python.org/3/library/typing.html) where appropriate
- Maximum line length: 88 characters

### Code Quality Tools

Run these before committing:

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run tests
python tests/run_tests.py
```

## 📝 Development Guidelines

### Architecture Principles

1. **Modular Design**: Keep components focused and loosely coupled
2. **Type Safety**: Use type hints and validate inputs
3. **Error Handling**: Graceful degradation with user-friendly messages
4. **Performance**: Consider memory usage and startup time
5. **Accessibility**: Support keyboard navigation and screen readers

### Adding New Features

1. **Update Specification**: First update the feature specification
2. **Add Tests**: Write tests before implementing (TDD)
3. **Implement Feature**: Write clean, testable code
4. **Update Documentation**: Update README, CHANGELOG, and user guides
5. **Test Manually**: Verify the feature works as expected

### File Organization

```
src/
├── menu/           # Main application modules
│   ├── models.py   # Data models and types
│   ├── config.py   # Configuration management
│   ├── window.py   # GTK window implementation
│   ├── button.py   # Button widgets
│   ├── launcher.py # Command execution
│   └── app.py      # Main application
├── utils/          # Utility modules
│   ├── cache.py    # Icon caching
│   └── validation.py# Configuration validation
└── main.py         # Entry point
```

### Adding New Button Types

To add a new command execution type:

1. **Update Enum**: Add to `CommandType` in `models.py`
2. **Update Validator**: Add validation logic in `launcher.py`
3. **Update Tests**: Add tests for the new type
4. **Update Documentation**: Update configuration examples

### Adding New Visual Themes

1. **Add Theme Options**: Update default configuration in `data/default.json`
2. **Update CSS**: Add new theme classes in `style.css`
3. **Update Models**: Add theme options to `ThemeConfig`
4. **Test Themes**: Verify themes render correctly

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test file
python -m unittest tests.test_config

# Run with coverage
pip install pytest-cov
pytest --cov=src tests/
```

### Writing Tests

- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies when needed
- Include performance tests for critical paths
- Test edge cases and error conditions

### Test Coverage

- Aim for >80% code coverage
- Focus on critical paths and error handling
- Include integration tests for user workflows
- Test configuration validation thoroughly

## 📦 Building and Packaging

### Building from Source

```bash
# Build wheel package
python -m build

# Install locally
pip install dist/fredon_menu-*.whl
```

### Creating Arch Linux Package

```bash
# Create package
makepkg -s

# Install package
sudo pacman -U fredon-menu-*.pkg.tar.zst
```

### Testing Package

```bash
# Test in clean environment
docker run -it archlinux bash
# Install dependencies and package in container
```

## 📖 Documentation

### Updating Documentation

- **README.md**: Installation, basic usage, troubleshooting
- **CHANGELOG.md**: Version history and release notes
- **CONTRIBUTING.md**: Development guidelines (this file)
- **API Documentation**: Code comments and docstrings
- **User Guide**: Detailed usage examples and configuration

### Documentation Style

- Use clear, concise language
- Include code examples for all major features
- Add screenshots and diagrams where helpful
- Keep documentation up to date with code changes

## 🔀 Release Process

### Preparing a Release

1. **Update Version**: Update version in `__init__.py`
2. **Update CHANGELOG**: Add release notes
3. **Run Tests**: Ensure all tests pass
4. **Update Documentation**: Verify docs are current
5. **Tag Release**: Create git tag with version number
6. **Create GitHub Release**: Upload built assets

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version number updated
- [ ] Git tag created
- [ ] GitHub release created
- [ ] AUR package updated
- [ ] Documentation website updated

## 🏆 Code Review Process

### Review Guidelines

Reviewers should check for:
- **Functionality**: Does the code work as intended?
- **Security**: Are there any security vulnerabilities?
- **Performance**: Will this impact performance negatively?
- **Maintainability**: Is the code clear and well-documented?
- **Tests**: Are tests comprehensive and correct?
- **Documentation**: Is documentation updated?

### Review Etiquette

- Be constructive and specific in feedback
- Explain reasoning behind suggestions
- Acknowledge good code and design decisions
- Focus on the code, not the author
- Ask questions to understand context

## 🌐 Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Documentation**: User guides and tutorials
- **Wiki**: Community-maintained documentation

### Code of Conduct

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions:
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive contributions
- Resolve conflicts respectfully

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor statistics
- Special recognition for major features

## 📞 Getting Help

If you need help contributing:

1. **Read Documentation**: Check existing docs first
2. **Search Issues**: Look for similar discussions
3. **Ask Questions**: Use GitHub Discussions for general questions
4. **Contact Maintainers**: Reach out via issues for specific help

## 🎉 Thank You

Thank you for contributing to Fredon Menu! Your contributions help make this project better for everyone.

---

*Last updated: 2025-10-25*