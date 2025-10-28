# Contributing Guidelines

Thank you for considering contributing to the AI Resume & LinkedIn Analyzer!

## Code of Conduct

Be respectful, inclusive, and constructive.

## How to Contribute

### Reporting Bugs

Use GitHub Issues with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- System information
- Screenshots if applicable

### Suggesting Features

Open an issue with:
- Feature description
- Use case and benefits
- Potential implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Follow code style**
   ```bash
   black src/ app/
   isort src/ app/
   flake8 src/ app/
   ```
5. **Write tests**
   ```bash
   pytest tests/
   ```
6. **Commit with clear messages**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
7. **Push and create PR**

## Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install
```

## Code Standards

### Python Style
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Maximum line length: 100 characters

### Commit Messages
Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance

### Testing
- Write unit tests for new features
- Maintain >80% code coverage
- Test edge cases

## Project Structure

```
src/          # Core business logic
app/          # Streamlit application
api/          # FastAPI backend
tests/        # Test suite
docs/         # Documentation
scripts/      # Utility scripts
```

## Questions?

Open an issue or reach out to maintainers.

---

**Happy Contributing! 🚀**