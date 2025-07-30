# pyconverters_isako

[![license](https://img.shields.io/github/license/oterrier/pyconverters_isako)](https://github.com/oterrier/pyconverters_isako/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyconverters_isako/workflows/tests/badge.svg)](https://github.com/oterrier/pyconverters_isako/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyconverters_isako)](https://codecov.io/gh/oterrier/pyconverters_isako)
[![docs](https://img.shields.io/readthedocs/pyconverters_isako)](https://pyconverters_isako.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyconverters_isako)](https://pypi.org/project/pyconverters_isako/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyconverters_isako)](https://pypi.org/project/pyconverters_isako/)

Convert PDF to structured text using [Isako](https://github.com/kermitt2/isako)

## Installation

You can simply `pip install pyconverters_isako`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyconverters_isako
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
