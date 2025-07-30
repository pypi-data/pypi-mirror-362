# Contributing to WMCoreDB

Thank you for your interest in contributing to WMCoreDB! This document provides guidelines and instructions for contributing to the project.

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for our commit messages. This helps us maintain a clear and consistent changelog and makes it easier to generate release notes automatically.

### Commit Message Format

Each commit message should follow this format:

```
<type>(<scope>): <subject>

<body>
```

### Types

The following types are allowed:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries

### Scopes

The scope is optional and should be a noun describing the part of the codebase affected by the change. For example:

- `db`: Database schema changes
- `ci`: CI/CD pipeline changes
- `docs`: Documentation changes

### Examples

```
feat(db): add new table for job tracking
fix(ci): correct SQL linting workflow
docs: update README with new features
style: format SQL files according to standards
```

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH) for our releases. You can use either format for tags:

- `1.0.0` (PyPI-friendly)
- `v1.0.0` (GitHub convention)

### Automatic Release Notes

When you create a new tag, our GitHub Actions workflow will automatically:

1. Generate a changelog based on commit messages
2. Create a GitHub release with the generated notes
3. Update the CHANGELOG.md file

The changelog will group commits by type and include:
- Features
- Bug Fixes
- Documentation
- Code Style
- Code Refactoring
- Performance Improvements
- Tests
- Maintenance

### Creating a Release

To create a new release:

1. Make sure all your commits follow the conventional commit format
2. Create a new tag:
   ```bash
   git tag -a 1.0.0 -m "Release 1.0.0"
   ```
3. Push the tag:
   ```bash
   git push origin 1.0.0
   ```

The GitHub Actions workflow will automatically create the release and update the changelog.

## Development Workflow

1. Create a new branch for your feature or fix
2. Make your changes following the commit message guidelines
3. Push your changes and create a pull request
4. Once approved, your changes will be merged into the main branch

## Code Style

### SQL Files

- Follow the SQLFluff rules defined in `.sqlfluff`
- For Oracle-specific files, follow the rules in `.sqlfluff.oracle`
- Use consistent indentation and formatting

### Python Files

- Follow PEP 8 style guidelines
- Use descriptive variable names
- Include docstrings for functions and classes
- Write unit tests for new functionality

## Questions?

If you have any questions about contributing, please open an issue in the repository. 