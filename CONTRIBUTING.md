# Contributing to PhD Deep Read Workflow

Thank you for your interest in contributing to the PhD Deep Read Workflow! This project aims to help researchers and PhD students process academic literature more efficiently, and we welcome contributions from the community.

## 🎯 How to Contribute

### Reporting Bugs
- Check if the bug has already been reported in [Issues](https://github.com/heleninsights-dot/phd-deepread-workflow/issues)
- If not, create a new issue with:
  - A clear, descriptive title
  - Steps to reproduce the bug
  - Expected vs actual behavior
  - Screenshots if applicable
  - Your environment (OS, Python version, installed packages)

### Suggesting Features
- Check if the feature has already been requested
- Create a new issue with:
  - A clear description of the feature
  - Why this feature would be useful
  - Any implementation ideas you have

### Contributing Code
1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Write or update tests** if applicable
5. **Ensure code quality** (run `black`, `flake8`, `mypy`)
6. **Commit changes** (`git commit -m 'Add amazing feature'`)
7. **Push to branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

## 🏗️ Development Setup

### Prerequisites
- Python 3.10+
- Git
- Tesseract OCR (optional, for development testing)

### Setup Steps
```bash
# Clone your fork
git clone https://github.com/heleninsights-dot/phd-deepread-workflow.git
cd phd-deepread-workflow

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=scripts --cov-report=html

# Run specific test file
pytest tests/test_extract.py -v
```

### Code Quality Tools
```bash
# Format code with black
black scripts/ tests/

# Sort imports with isort
isort scripts/ tests/

# Check for style issues with flake8
flake8 scripts/ tests/

# Type checking with mypy
mypy scripts/
```

## 📁 Project Structure

```
phd-deepread-workflow/
├── scripts/           # Core Python scripts
│   ├── extract.py    # PDF extraction with decision tree
│   ├── generate.py   # Structured note generation
│   ├── canvas.py     # JSON Canvas creation
│   ├── verify.py     # Quality verification
│   ├── setup.sh      # Environment setup
│   └── batch.sh      # Batch processing
├── templates/        # Template files
│   └── .clauderules  # Literature note template
├── docs/            # Documentation
│   ├── workflow-guide.md
│   └── decision-tree.md
├── examples/        # Example outputs
│   ├── example-output.md
│   └── example-canvas.canvas
├── tests/           # Test files
├── config/          # Configuration files (planned)
└── logs/            # Log files (optional)
```

## 📝 Code Style

### Python Code
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for function signatures
- Write docstrings for public functions/classes
- Keep functions focused and small (<50 lines)

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add new extraction parameter
fix: handle empty PDF files
docs: update installation instructions
test: add tests for OCR fallback
refactor: simplify decision tree logic
chore: update dependencies
```

### Documentation
- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Keep documentation in sync with code

## 🧪 Testing Guidelines

### Writing Tests
- Tests go in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies (Tesseract, PyMuPDF)
- Include integration tests for the full workflow

### Test Structure
```python
def test_extract_searchable_pdf():
    """Test extraction of PDF with searchable text."""
    # Arrange
    pdf_path = "tests/data/searchable.pdf"

    # Act
    result = extract_pdf(pdf_path)

    # Assert
    assert result["success"] == True
    assert result["pages"] > 0
```

## 🔍 Review Process

1. **Pull Request Description**: Clearly describe what changes were made and why
2. **Code Review**: At least one maintainer will review your code
3. **CI Checks**: All tests must pass, code quality checks must pass
4. **Merge**: Once approved, a maintainer will merge your PR

### What Reviewers Look For
- Code correctness and functionality
- Adherence to project style and conventions
- Test coverage for new code
- Documentation updates
- Backward compatibility

## 🚀 Advanced Contributions

### Adding New Features
1. Discuss the feature in an issue first
2. Design the API/user interface
3. Implement with tests and documentation
4. Consider backward compatibility
5. Update configuration if needed

### Improving Performance
- Profile before optimizing
- Add benchmarks to track improvements
- Document performance characteristics
- Consider memory usage and scalability

### Enhancing Documentation
- Fix typos and unclear explanations
- Add more examples
- Create tutorials or guides
- Improve API documentation

## 🐛 Troubleshooting Development Issues

### Common Problems
**Tests failing:**
- Check Python version compatibility
- Verify dependencies are installed
- Ensure test data exists

**Code quality checks failing:**
- Run `black` and `isort` to auto-format
- Fix flake8 warnings
- Address mypy type errors

**Environment issues:**
- Recreate virtual environment
- Update pip: `pip install --upgrade pip`
- Clear cache: `rm -rf .pytest_cache/ .mypy_cache/`

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: Contact the maintainers at [heleninsights@gmail.com](mailto:heleninsights@gmail.com)

## 🙏 Acknowledgments

Thank you for contributing to make PhD Deep Read Workflow better for everyone in the academic community!

---

*This contributing guide is adapted from several open source projects and is licensed under the same terms as the main project.*