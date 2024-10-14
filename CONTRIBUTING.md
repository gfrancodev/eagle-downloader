# Contributing to Eagle Downloader

First off, thank you for considering contributing to **Eagle Downloader**! 🎉 Your efforts are greatly appreciated and help make this project better for everyone.

## Table of Contents

- [How Can I Contribute?](#how-can-i-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Pull Requests](#pull-requests)
- [Code Style](#code-style)
- [Testing](#testing)
- [Continuous Integration](#continuous-integration)
- [License](#license)
- [Contact](#contact)

## How Can I Contribute?

There are several ways you can contribute to **Eagle Downloader**:

- **Reporting Bugs**: If you find a bug, please [open an issue](https://github.com/gfrancodev/eagle-downloader/issues/new/choose) with a clear description and steps to reproduce.
- **Suggesting Enhancements**: Have an idea to improve the project? Feel free to [suggest an enhancement](https://github.com/gfrancodev/eagle-downloader/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=).
- **Code Contributions**: Submit pull requests to fix bugs or add new features. Please follow the guidelines below to ensure a smooth review process.
- **Documentation**: Help improve the project documentation by updating the `README.md`, creating tutorials, or improving inline comments.

## Reporting Bugs

Before reporting a bug, please ensure that:

1. **Reproduce the Issue**: Verify that the issue exists by following the steps you provide.
2. **Provide Details**: Include information such as your operating system, Python version, and any relevant logs or error messages.
3. **Check Existing Issues**: Ensure that the bug hasn't already been reported or addressed in recent commits.

## Suggesting Enhancements

When suggesting an enhancement, please:

1. **Describe the Feature**: Clearly explain what the feature is and why it would be beneficial.
2. **Provide Examples**: Use screenshots or code snippets to illustrate your idea.
3. **Discuss Alternatives**: Mention any alternative solutions you considered.

## Pull Requests

We welcome pull requests! Here's how to get started:

1. **Fork the Repository**: Click the "Fork" button at the top-right corner of the repository page.
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/gfrancodev/eagle-downloader.git
   cd eagle-downloader
   ```
3. **Create a New Branch**:
   ```bash
   git checkout -b feature/YourFeatureName
   ```
4. **Make Your Changes**: Implement your feature or bug fix.
5. **Run Tests and Linting**:
   ```bash
   make test-coverage
   make lint
   make format
   ```
6. **Commit Your Changes**:
   ```bash
   git commit -m "Add feature: YourFeatureDescription"
   ```
7. **Push to Your Fork**:
   ```bash
   git push origin feature/YourFeatureName
   ```
8. **Open a Pull Request**: Navigate to the original repository and click "Compare & pull request". Provide a clear description of your changes.

### Pull Request Guidelines

- **Describe Your Changes**: Clearly explain what your PR does and why.
- **Link Issues**: Reference any related issues (e.g., `Closes #123`).
- **Keep It Focused**: Aim for one feature or fix per PR to make reviews easier.
- **Ensure Code Quality**: Follow the project's coding standards and pass all tests.

## Code Style

We follow [PEP 8](https://pep8.org/) for Python code style. Please ensure your code adheres to these guidelines by running:

```bash
make lint
make format
```

## Testing

Before submitting a pull request, make sure all tests pass and coverage is maintained:

```bash
make test
make test-coverage
```

- **Adding Tests**: If you add a feature or fix a bug, please include appropriate tests.
- **Coverage Threshold**: Strive to maintain or improve the existing test coverage.

## Continuous Integration

We use GitHub Actions for continuous integration. All pull requests will automatically run the CI pipeline to verify builds, run tests, and ensure code quality.

- **Failing Builds**: If the CI pipeline fails, please address the issues before requesting a review.
- **Re-running CI**: You can manually re-run workflows from the Actions tab if needed.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or need assistance, feel free to [open an issue](https://github.com/gfrancodev/eagle-downloader/issues) or reach out to the maintainer at [contact@gfrancodev.com](mailto:contact@gfrancodev.com).