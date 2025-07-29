# jbussdieker-project

A modern Python development toolkit plugin for generating complete Python project structures using the jbussdieker CLI framework. This plugin creates fully configured Python projects with CI/CD workflows, testing setup, and all necessary development files.

## 🚀 Features

- **Complete Project Generation**: Creates fully structured Python projects with all necessary files
- **CI/CD Integration**: Includes GitHub Actions workflows for testing and publishing
- **Testing Setup**: Pre-configured test structure with pytest
- **Modern Python Configuration**: Uses pyproject.toml for modern Python packaging
- **License and Documentation**: Automatically generates LICENSE and README files
- **Git Integration**: Includes .gitignore and proper Git setup
- **Customizable Templates**: Uses configurable templates for all generated files
- **Multi-Environment Support**: Works across different Python versions and operating systems

## 📦 Installation

```bash
pip install jbussdieker-project --upgrade
```

## 🔧 Prerequisites

- Python 3.9 or higher
- jbussdieker CLI framework
- Git (for version control integration)

## 🎯 Usage

### Basic Usage

Create a new Python project:

```bash
jbussdieker project my-awesome-project
```

This will create a complete project structure:

```
my-awesome-project/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── publish.yml
├── src/
│   └── my-awesome-project/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_my-awesome-project.py
├── LICENSE
├── Makefile
├── README.md
├── pyproject.toml
└── .gitignore
```

### Generated Project Structure

The plugin generates a complete Python project with:

- **Source Code**: Properly structured `src/` layout
- **Testing**: pytest configuration and test files
- **CI/CD**: GitHub Actions for testing and publishing
- **Documentation**: README and license files
- **Build System**: Modern pyproject.toml configuration
- **Development Tools**: Makefile with common development commands

## 🔍 Generated Files

### Core Project Files

- `pyproject.toml`: Modern Python project configuration
- `README.md`: Project documentation template
- `LICENSE`: MIT license with your name
- `.gitignore`: Python-specific Git ignore rules
- `Makefile`: Development commands and shortcuts

### CI/CD Workflows

- `.github/workflows/ci.yml`: Automated testing workflow
- `.github/workflows/publish.yml`: Automated publishing to PyPI

### Source Structure

- `src/<project_name>/__init__.py`: Main package initialization
- `tests/`: Complete testing structure with pytest

## 🛠️ Development

This plugin is part of the jbussdieker ecosystem. It integrates seamlessly with the jbussdieker CLI framework.

### Project Structure

```
src/jbussdieker/project/
├── __init__.py
├── cli.py          # CLI interface and argument parsing
├── generator.py    # Core project generation logic
├── git_utils.py    # Git integration utilities
├── template_loader.py # Template loading and substitution
└── templates/      # Project template files
    ├── pyproject.toml.tpl
    ├── README.md.tpl
    ├── LICENSE.tpl
    ├── Makefile.tpl
    ├── ci.yml.tpl
    ├── publish.yml.tpl
    └── ...
```

### Template System

The plugin uses a flexible template system that supports variable substitution for:
- Project name and description
- User information (name, email)
- GitHub organization
- Default branch name
- Version information

## 📝 License

This project is licensed under **MIT**.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Related

- [jbussdieker](https://pypi.org/project/jbussdieker/) - The main CLI framework
- [Python Packaging User Guide](https://packaging.python.org/) - Python packaging best practices
