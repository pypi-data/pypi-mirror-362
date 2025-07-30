# 🚀 Easeon - Python Package Manager

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) 
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-green)](https://pypi.org/project/easeon/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Easeon is a powerful Python package manager that simplifies package installation and virtual environment management with a clean, intuitive API.

## ✨ Features

- 🏗️ **Automatic Virtual Environments** - Create and manage Python environments with ease
- 📦 **Multiple Installation Sources** - Install from `.txt`, `.csv`, or Python lists
- 🔍 **TestPyPI Support** - Seamlessly switch between PyPI and TestPyPI
- 📝 **Comprehensive Logging** - Built-in logging to file and/or console
- 🛠️ **Developer Friendly** - Type hints, docstrings, and clean architecture
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux

## 📦 Installation

Install from PyPI:

```bash
pip install easeon
```

Or for the latest development version:

```bash
pip install git+https://github.com/buHtiG20241217/Easeon.git
```

## 🚀 Quick Start

### Basic Usage

#### Simplified API (Recommended)

```python
from easeon import EaseonInstaller

# Chainable API for easy package installation
installer = (EaseonInstaller()
    .get_list(["requests", "numpy>=1.21.0"])  # Install from list
    .get_txt("requirements.txt")              # Add packages from requirements.txt
    .get_csv("packages.csv")                  # Add packages from CSV file
    .install()                                # Execute installation
)

# View installation logs
print(installer.get_logs())
```

#### Traditional API

```python
from easeon import EaseonInstaller

# Create a new virtual environment and install packages
installer = EaseonInstaller(
    env_name="myenv",  # Creates a virtual environment named 'myenv'
    log_destination="console"  # Log to console
)

# Install packages
installer.install_from_list(["requests", "numpy>=1.21.0"])

# View installation logs
print(installer.get_logs())
```

### Advanced Usage

```python
from pathlib import Path
from easeon import EaseonInstaller

# Custom configuration
installer = EaseonInstaller(
    env_name="dev_env",
    use_test_pypi=True,  # Use TestPyPI
    use_test_pypi_easeon=True,  # Use TestPyPI only for Easeon
    log_destination=Path("install.log")  # Log to file
)

# Install from requirements.txt
installer.install_from_txt("requirements.txt")

# Install additional packages
installer.install_from_list(["pytest", "black", "mypy"])
```

## 📚 Documentation

### EaseonInstaller Class

The main class for managing package installations and virtual environments.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `auto_create_venv` | `bool` | `True` | Automatically create virtual environment if `env_name` is provided |
| `env_name` | `Optional[str]` | `None` | Name of the virtual environment to create/use |
| `use_test_pypi` | `bool` | `False` | Use TestPyPI for all packages |
| `use_test_pypi_easeon` | `bool` | `False` | Use TestPyPI only for Easeon package |
| `log_destination` | `Optional[Union[str, Path]]` | `None` | Where to write logs (`None`, file path, or "console") |

#### Methods

##### Simplified API Methods
- `get_list(packages: List[str]) -> EaseonInstaller` - Set package list from a Python list
- `get_txt(path: str) -> EaseonInstaller` - Add packages from a requirements.txt file
- `get_csv(path: str) -> EaseonInstaller` - Add packages from a CSV file (first column)
- `install() -> None` - Execute the installation
- `get_logs() -> str` - Retrieve complete installation logs

##### Traditional API Methods
- `install_from_list(pkg_list: List[str])` - Install packages from a list
- `install_from_txt(path: str)` - Install packages from a requirements.txt file
- `install_from_csv(path: str)` - Install packages from a CSV file
- `get_logs() -> str` - Retrieve complete installation logs (returns empty string if no logs available)

### Virtual Environment Management

Easeon makes it easy to work with virtual environments:

```python
# Create and use a virtual environment
installer = EaseonInstaller(env_name="myenv")

# Use existing environment
installer = EaseonInstaller(auto_create_venv=False)
```

## 🔍 Logging

Easeon provides flexible logging options:

```python
# Log to console
EaseonInstaller(log_destination="console")

# Log to file
EaseonInstaller(log_destination="install.log")

# Default: Logs to ~/easeon_install.log
EaseonInstaller()
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📁 File Format Examples

### `packages.txt`
```txt
# Commented line
requests
numpy==1.24.0
pandas
```

### `packages.csv`
```csv
requests
flask
beautifulsoup4
```

---

## 🧪 Testing

To run all tests:
```bash
pytest --maxfail=3 --disable-warnings -q
```
Or with unittest:
```bash
python -m unittest discover tests
```

---


## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Please:
- Fork the repo and create a feature branch
- Add or update tests for new features
- Update `feature_status.json` as appropriate
- Open a pull request describing your changes

---

## 👤 Author

**Kiran Soorya R.S**  
📧 hemalathakiransoorya2099@gmail.com

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌐 Links

- [PyPI Package](https://pypi.org/project/easeon/)
- [Test PyPI](https://test.pypi.org/project/easeon/)

> ⭐ Feedback and stars are appreciated!
--

## 📁 File Format Examples

### `packages.txt`

```txt
# Commented line
requests
numpy==1.24.0
pandas
```

### `packages.csv`

```csv
requests
flask
beautifulsoup4
```

---

## 🧪 Testing

To run unit tests:

```bash
python -m unittest discover tests
```

---

## 👤 Author

**Kiran Soorya R.S**  
📧 hemalathakiransoorya2099@gmail.com

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌐 Links

- 📦 [PyPI Package](https://pypi.org/project/easeon/)
- 🧪 [Test PyPI](https://test.pypi.org/project/easeon/)

---

> Contributions, feedback, and stars 🌟 are welcome!
