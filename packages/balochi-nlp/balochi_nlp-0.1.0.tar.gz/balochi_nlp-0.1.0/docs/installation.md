# Installation Guide

This guide will help you install and set up Balochi NLP on your system.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation Methods

### 1. Using pip (Recommended)

```bash
pip install balochi-nlp
```

### 2. From Source (Development)

1. Clone the repository:
```bash
git clone https://github.com/hafeezBaluch/balochi-nlp.git
cd balochi-nlp
```

2. Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the package in development mode:
```bash
pip install -e ".[dev]"
```

## Verifying Installation

To verify that Balochi NLP is installed correctly, run Python and try importing the package:

```python
import balochi_nlp
print(balochi_nlp.__version__)
```

## Dependencies

The following dependencies will be automatically installed:

### Core Dependencies
- numpy>=1.21.0
- pandas>=1.3.0
- nltk>=3.6.0
- scikit-learn>=0.24.0
- regex>=2023.0.0
- tqdm>=4.65.0

### Development Dependencies
- pytest>=7.0
- pytest-cov>=4.0
- black>=22.0
- isort>=5.0
- flake8>=4.0
- mypy>=0.9
- tox>=3.24

## Common Issues and Solutions

### 1. Python Version Compatibility
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### 2. Permission Issues
If you encounter permission errors during installation:

**Windows:**
- Run PowerShell or Command Prompt as Administrator
- Use `--user` flag: `pip install --user balochi-nlp`

**macOS/Linux:**
- Use `sudo` (system-wide installation): `sudo pip install balochi-nlp`
- Use `--user` flag: `pip install --user balochi-nlp`

### 3. Virtual Environment Issues

If you have trouble with virtual environments:

**Windows PowerShell:**
If you can't activate the virtual environment, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
If `venv` is not found:
```bash
python3 -m pip install --user virtualenv
```

## Getting Help

If you encounter any issues during installation:

1. Check our [GitHub Issues](https://github.com/hafeezBaluch/balochi-nlp/issues)
2. Create a new issue if your problem isn't already reported
3. Contact the maintainer: Hafeez Baloch (hafeezullahhassan2019@gmail.com) 