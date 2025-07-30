<p align="center">
   <h1 align="center"><b>PyRequire</b></h1>
</p>

[![License](https://img.shields.io/badge/license-BSD--3--Clause-green)](https://github.com/keurfonluu/pyrequire/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/keurfonluu/pyrequire?style=flat&logo=github)](https://github.com/keurfonluu/pyrequire)
[![Pyversions](https://img.shields.io/pypi/pyversions/pyrequire.svg?style=flat)](https://pypi.org/pypi/pyrequire/)
[![Version](https://img.shields.io/pypi/v/pyrequire.svg?style=flat)](https://pypi.org/project/pyrequire)
[![Downloads](https://pepy.tech/badge/pyrequire)](https://pepy.tech/project/pyrequire)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)

A bunch of decorators for checking specific requirements of Python functions at runtime.

## Features

- Simple decorators to enforce required Python version or package versions at runtime
- Flexible version specification using standard comparison operators (e.g., >=, <, ==)
- Lightweight, with no runtime dependencies
- Helps ensure reproducibility and compatibility in code execution

## Installation

The recommended way to install **pyrequire** is through the Python Package Index:

```bash
pip install pyrequire --user
```

Otherwise, clone and extract the package, then run from the package location:

```bash
pip install . --user
```

To test the integrity of the installed package, check out this repository and run:

```bash
pytest
```

## Examples

```python
from pyrequire import require_package, require_python

@require_python(">=3.9")
@require_package("foo>=1.2.3")
def bar():
    return
```