# Contributing to Shekar

Thank you for your interest in contributing to Shekar! We welcome contributions from the community and are grateful for your support in making Persian NLP more accessible.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. We expect all contributors to:

- Be respectful and considerate in communication
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing viewpoints and experiences
- Accept responsibility and apologize for mistakes

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Python version and operating system
- Shekar version (`pip show shekar`)
- Sample code or text that demonstrates the problem
- Error messages or stack traces

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- A clear description of the proposed feature
- Use cases and benefits
- Examples of how it would work
- Any relevant references or implementations in other libraries

### Contributing Code

We appreciate code contributions! Areas where you can help:

- Bug fixes
- New features or improvements
- Performance optimizations
- Better Persian language support
- Documentation improvements
- Test coverage expansion
- Model improvements

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/shekar.git
   cd shekar
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/amirivojdan/shekar.git
   ```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- git
- (Optional) CUDA Toolkit for GPU support

### Installing uv

If you don't have uv installed:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Installation

1. Clone the repository (if you haven't already)

2. Install development dependencies with uv:
   ```bash
   uv sync --all-extras
   ```

### Project Structure

```
shekar/
├── shekar/              # Main package
│   ├── preprocessing/   # Text preprocessing components
│   ├── tokenizers/      # Tokenization modules
│   ├── embeddings/      # Embedding models
│   ├── stemmer/         # Stemming functionality
│   ├── lemmatizer/      # Lemmatization functionality
│   ├── pos_tagger/      # POS tagging
│   ├── ner/             # Named entity recognition
│   └── ...
├── tests/               # Test suite
├── docs/                # Documentation
└── examples/            # Example scripts
```

## Making Changes

### Branching Strategy

1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. Use descriptive branch names:
   - `feature/add-lemmatization`
   - `fix/tokenizer-unicode-issue`
   - `docs/update-embedding-examples`
   - `test/add-ner-tests`

### Commit Messages

Write clear, concise commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line: brief summary (50 chars or less)
- Follow with detailed explanation if needed

Examples:
```
Add support for custom stopword lists

- Allow users to provide custom stopword files
- Add validation for stopword format
- Update documentation with examples
```

### Code Quality

- Write clean, readable code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Keep functions focused and modular
- Avoid breaking existing APIs without discussion

### Persian Language Considerations

When working on Persian NLP features:

- Test with various Persian texts including informal writing
- Consider Zero Width Non-Joiner (ZWNJ) usage
- Handle both Persian and Arabic character variants
- Test with different diacritic combinations
- Consider right-to-left text rendering issues

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_tokenizer.py

# Run with coverage
uv run pytest --cov=shekar tests/
```

### Writing Tests

- Write tests for new features and bug fixes
- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names
- Include both positive and negative test cases
- Test edge cases and Persian-specific scenarios

Example test structure:
```python
def test_normalizer_removes_diacritics():
    normalizer = Normalizer()
    text = "سَلام"
    expected = "سلام"
    assert normalizer(text) == expected
```

## Submitting Changes

### Pull Request Process

1. **Update your branch** with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference any related issues (e.g., "Fixes #123")
   - Screenshots or examples if applicable
   - Notes on testing performed

4. **Review process**:
   - Maintainers will review your PR
   - Address any feedback or requested changes
   - Once approved, your PR will be merged

### Pull Request Checklist

- [ ] Code follows the project's style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated if needed
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main

## Style Guidelines

### Python Code Style

- Follow PEP 8
- Maximum line length: 100 characters
- Use type hints where appropriate
- Use meaningful variable names

### Documentation Style

- Use Google-style docstrings
- Include parameter types and return values
- Provide usage examples
- Write in clear, simple English

Example:
```python
def normalize_text(text: str, remove_diacritics: bool = True) -> str:
    """Normalize Persian text.
    
    Args:
        text: Input Persian text to normalize
        remove_diacritics: Whether to remove diacritical marks
        
    Returns:
        Normalized Persian text
        
    Example:
        >>> normalize_text("سَلام")
        'سلام'
    """
    pass
```

## Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Add docstrings to new code
- Update examples if APIs change
- Consider adding tutorials for complex features

### Building Documentation

Documentation is built using MkDocs:

```bash
# Build documentation
uv run mkdocs build

# Serve documentation locally (with auto-reload)
uv run mkdocs serve
```

Then open http://127.0.0.1:8000 in your browser to view the documentation.

## Community

### Getting Help

- Open an issue for questions
- Check existing issues and documentation first
- Be patient and respectful

### Recognition

Contributors will be recognized in:
- Project README
- Release notes
- GitHub contributors page

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the "question" label
- Reach out to the maintainers

---

Thank you for contributing to Shekar! Your efforts help make Persian NLP more accessible to everyone. 🙏

<p align="center"><em>Persian is Sugar</em></p>
<p align="center" dir="rtl"><em dir="rtl">"فارسی شکر است"</em></p>
