# Contributing to DriveDiff

We love your input! We want to make contributing to DriveDiff as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/yourusername/DriveDiff/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/DriveDiff/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/DriveDiff.git
   cd DriveDiff
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If development dependencies exist
   ```

4. **Run tests**
   ```bash
   python -m pytest tests/
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

## Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and modular
- Use type hints where appropriate

### Example Code Style
```python
def compare_files(left_path: str, right_path: str) -> FileDifference:
    """
    Compare two files and return difference information.
    
    Args:
        left_path: Path to the left file
        right_path: Path to the right file
        
    Returns:
        FileDifference object containing comparison results
    """
    # Implementation here
    pass
```

## Project Structure Guidelines

- **Core logic** goes in `src/core/`
- **GUI components** go in `src/gui/`
- **Utilities** go in `src/utils/`
- **Tests** go in `tests/` with matching structure
- **Documentation** goes in root or `docs/`

## Testing Guidelines

- Write tests for new functionality
- Ensure existing tests pass
- Use descriptive test names
- Test both success and error cases
- Mock external dependencies

### Example Test
```python
def test_file_comparison_identical():
    """Test that identical files are correctly identified."""
    # Arrange
    left_file = create_test_file("content")
    right_file = create_test_file("content")
    
    # Act
    result = compare_files(left_file, right_file)
    
    # Assert
    assert result.status == "identical"
```

## Feature Requests

We use GitHub issues to track feature requests. When proposing a new feature:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** the feature would solve
3. **Provide examples** of how it would be used
4. **Consider alternatives** you've thought of
5. **Be open to discussion** about implementation

## Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add comments for complex logic
- Update CHANGELOG.md for all changes

## Commit Message Guidelines

Use clear and meaningful commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Examples
```
Add SHA256 hash comparison for file verification

- Implement hash-based file comparison
- Add binary file detection
- Update tests for new comparison logic

Fixes #123
```

## Code Review Process

1. All submissions require review before merging
2. Maintainers will review pull requests
3. Address review feedback promptly
4. Be open to suggestions and improvements
5. Ensure CI passes before requesting review

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers get started
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)

## Getting Help

- Check existing [issues](https://github.com/yourusername/DriveDiff/issues)
- Read the [documentation](README.md)
- Ask questions in new issues
- Join discussions in existing issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
