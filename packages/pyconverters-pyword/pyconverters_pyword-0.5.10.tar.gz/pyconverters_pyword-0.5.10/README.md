# pyconverters_pyword

[![license](https://img.shields.io/github/license/oterrier/pyconverters_pyword)](https://github.com/oterrier/pyconverters_pyword/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyconverters_pyword/workflows/tests/badge.svg)](https://github.com/oterrier/pyconverters_pyword/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyconverters_pyword)](https://codecov.io/gh/oterrier/pyconverters_pyword)
[![docs](https://img.shields.io/readthedocs/pyconverters_pyword)](https://pyconverters_pyword.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyconverters_pyword)](https://pypi.org/project/pyconverters_pyword/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyconverters_pyword)](https://pypi.org/project/pyconverters_pyword/)

Convert OCRized PDF to text using [PyWord](https://github.com/pyword/PyWord)

## Installation

You can simply `pip install pyconverters_pyword`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyconverters_pyword
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
