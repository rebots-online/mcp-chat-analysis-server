# Contributing to MCP Chat Analysis Server

We love your input! We want to make contributing to the MCP Chat Analysis Server as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Pull Request Process

1. Update the README.md with details of changes to the interface
2. Update the docs/ with any new information
3. The PR will be merged once you have the sign-off of two other developers

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker]

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/rebots-online/mcp-chat-analysis-server/issues/new).

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Use a Consistent Coding Style

* Use [Black](https://github.com/psf/black) for Python code formatting
* Use type hints for Python code
* Keep line length to 100 characters
* Write docstrings for all public methods

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## References

This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/a9316a723f9e918afde44dea68b5f9f39b7d9b00/CONTRIBUTING.md).

## Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

4. Run tests:
```bash
pytest tests/
```

## Code Review Process

The core team looks at Pull Requests on a regular basis. After feedback has been given we expect responses within two weeks. After two weeks we may close the PR if it isn't showing any activity.

## Community

Discussions about the Open Source project happen in the Issues and Pull Requests sections on GitHub. Anybody is welcome to join these conversations.

## Documentation

We use [Google style](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for formatting the docstrings:

```python
def fetch_something(param1: str, param2: int) -> Dict[str, Any]:
    """Fetches something.

    Args:
        param1: The first parameter.
        param2: The second parameter.

    Returns:
        A dict with some data.

    Raises:
        KeyError: If a key error occurs.
    """