# Applied Biostats Helper

A Python package that simplifies environment setup for the Applied Biostats course, particularly for Google Colab notebooks. This package replaces complex setup blocks with a single function call.

## Features

- **One-line environment setup** for Colab and local Jupyter notebooks
- **Automatic dependency management** (installs otter-grader if needed)
- **Seamless test file downloading** from GitHub repositories
- **Environment detection** (automatically detects Colab vs local)
- **Clean error handling** and user feedback

## Installation

### From GitHub (Recommended for testing)

```bash
pip install git+https://github.com/DamLabResources/applied-biostats-helper.git.
```

### From PyPI (when published)

```bash
pip install applied-biostats-helper
```

### Local Development

```bash
git clone https://github.com/DamLabResources/applied-biostats-helper.git
cd applied-biostats-helper
pip install -e .
```

## Quick Start

### Before (Complex setup block)

```python
# Setting up the Colab environment. DO NOT EDIT!
import os
import warnings
warnings.filterwarnings("ignore")

try:
    import otter
except ImportError:
    ! pip install -q otter-grader==4.0.0
    import otter

if not os.path.exists('walkthrough-tests'):
    zip_files = [f for f in os.listdir() if f.endswith('.zip')]
    assert len(zip_files)>0, 'Could not find any zip files!'
    assert len(zip_files)==1, 'Found multiple zip files!'
    ! unzip {zip_files[0]}

grader = otter.Notebook(colab=True, tests_dir='walkthrough-tests')
```

### After (Simple one-liner)

```python
from applied_biostats import setup_environment

grader = setup_environment('Module02_walkthrough')
```

## Usage

### Main Function: `setup_environment()`

The primary function that handles all setup tasks:

```python
from applied_biostats import setup_environment

# Basic usage
grader = setup_environment('Module02_walkthrough')

# With custom branch
grader = setup_environment('Module02_walkthrough',
                          branch='dev')

```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
- Open an issue on GitHub
- Contact the course instructors

## Changelog

### v0.1.0
- Initial release
- Basic environment setup functionality
- GitHub integration for test file downloads
- Colab and local Jupyter support 