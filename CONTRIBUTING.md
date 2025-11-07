# Contributing to Duck Console

First off, thank you for considering contributing to Duck Console! It's people like you that make Duck Console such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check [the issue list](https://github.com/Luc45-Pereira/duck-console/issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include any error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please provide:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints

## Development Process

1. Clone the repository
```bash
git clone https://github.com/Luc45-Pereira/duck-console.git
cd duck-console
```

2. Install development dependencies
```bash
poetry install
```

3. Create a branch
```bash
git checkout -b my-feature
```

4. Make your changes
* Write meaningful commit messages
* Follow the coding style
* Write tests for new features
* Update documentation as needed

5. Run tests
```bash
poetry run pytest
```

6. Submit a pull request
* Fill in the pull request template
* Do not include issue numbers in the PR title

## Testing

* Write test cases for any new functionality
* Run the full test suite before submitting
* Tests should be written using pytest
* Aim for high test coverage

## Documentation

* Keep docstrings up to date
* Follow Google-style docstring format
* Update README.md for user-facing changes
* Add examples for new features

## Code Style

* Follow PEP 8 guidelines
* Use type hints
* Run black for code formatting
* Sort imports using isort

## License

By contributing to Duck Console, you agree that your contributions will be licensed under the Apache License 2.0.