# Contributing to Rekha

Thank you for your interest in contributing to Rekha!
Our community is open to everyone and welcomes all kinds of contributions, no matter how small or large.
There are several ways you can contribute to the project:

- Identify and report any issues or bugs.
- Request or add new plot types.
- Suggest or implement new features.
- Improve documentation and examples.
- Add new themes or color palettes.

However, remember that contributions aren't just about code.
We believe in the power of community support; thus, answering queries, assisting others, and enhancing the documentation are highly regarded and beneficial contributions.

Finally, one of the most impactful ways to support us is by raising awareness about Rekha.
Talk about it in your blog posts, highlighting how it's driving your incredible projects.
Express your support on Twitter if Rekha aids you, or simply offer your appreciation by starring our repository.

## Setup for development

### Installation

1. Clone the repository:
```bash
git clone https://github.com/project-vajra/rekha.git
cd rekha
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e ".[dev]"
```

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=rekha --cov-report=html

# Run specific test file
pytest tests/test_plots.py
```

### Code formatting

We use several tools to maintain code quality:

```bash
# Format code
black rekha tests examples
isort rekha tests examples

# Lint code
pyright rekha

# Spell check
codespell
```

## Contributing Guidelines

### Issue Reporting

If you encounter a bug or have a feature request, please check our issues page first to see if someone else has already reported it.
If not, please file a new issue, providing as much relevant information as possible.

### Coding Style Guide

We follow [PEP 8](https://pep8.org/) and [Black](https://black.readthedocs.io/) formatting standards.

Key points:
- Use descriptive variable names
- Add type hints to all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Write tests for new functionality

### Pull Requests

When submitting a pull request:

1. Make sure your code has been rebased on top of the latest commit on the main branch.
2. Ensure code is properly formatted by running the formatting tools above.
3. Add tests for any new functionality.
4. Update documentation if needed.
5. Include a detailed description of the changes in the pull request.
   Explain why you made the changes you did.
   If your pull request fixes an open issue, please include a reference to it in the description.

### Code Reviews

All submissions, including submissions by project members, require a code review.
To make the review process as smooth as possible, please:

1. Keep your changes as concise as possible.
   If your pull request involves multiple unrelated changes, consider splitting it into separate pull requests.
2. Respond to all comments within a reasonable time frame.
   If a comment isn't clear or you disagree with a suggestion, feel free to ask for clarification or discuss the suggestion.

### Adding New Plot Types

When adding new plot types:

1. Follow the existing API patterns (similar to `line()`, `scatter()`, etc.)
2. Support both light and dark modes
3. Include grayscale printing support
4. Add comprehensive docstrings with examples
5. Include tests that cover the main functionality
6. Add examples to the examples directory

### Documentation

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples for existing functionality
- Improve API documentation
- Create tutorials for common use cases

## Development Philosophy

Rekha aims to be:

1. **Beautiful by default** - Plots should look professional without tweaking
2. **Simple API** - Common tasks should be one-liners
3. **Full control** - Complex customization should be possible
4. **Performance** - No unnecessary overhead
5. **Academic-ready** - Publication-quality output with fine controls

When contributing, please keep these principles in mind.

## Thank You

Finally, thank you for taking the time to read these guidelines and for your interest in contributing to Rekha.
Your contributions make Rekha a great tool for everyone!