# Contributing to OHLCV to Orderbook Converter

We welcome contributions to the OHLCV to Orderbook Converter project! This document provides guidelines for contributing.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of financial data structures (OHLCV, orderbooks)

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/ohlcv-to-orderbook.git
   cd ohlcv-to-orderbook
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions and methods
- Maintain compatibility with Python 3.8+
- All code comments and documentation should be in English

### Testing

Before submitting any changes:

1. Run the test suite:
   ```bash
   pytest
   ```

2. Check test coverage:
   ```bash
   pytest --cov=ohlcv_to_orderbook --cov-report=html
   ```

3. Run type checking:
   ```bash
   mypy ohlcv_to_orderbook
   ```

4. Ensure all tests pass and coverage remains above 90%

### Making Changes

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the code style guidelines
3. Add or update tests as necessary
4. Update documentation if needed
5. Commit your changes with a clear commit message:
   ```bash
   git commit -m "Add feature: clear description of what was added"
   ```

### Submitting Changes

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub with:
   - Clear title and description
   - Reference to any related issues
   - Description of changes made
   - Test results

## Types of Contributions

### Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Complete error traceback
- Minimal code example to reproduce the issue
- Expected vs actual behavior

### Feature Requests

For new features:
- Describe the use case
- Explain why it would be beneficial
- Consider backwards compatibility
- Provide examples if possible

### Code Contributions

We welcome:
- Bug fixes
- Performance improvements
- New features (after discussion in issues)
- Documentation improvements
- Test coverage improvements

## Code Review Process

1. All submissions require review before merging
2. Maintainers will review your code for:
   - Functionality and correctness
   - Code quality and style
   - Test coverage
   - Documentation completeness
3. Address feedback promptly
4. Once approved, maintainers will merge your PR

## Release Process

- Releases follow semantic versioning (SemVer)
- Changes are documented in the changelog
- All releases are tagged and published to PyPI

## Questions?

Feel free to open an issue for questions about contributing or join discussions in existing issues.

Thank you for contributing to OHLCV to Orderbook Converter!
