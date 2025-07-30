# pyprocessors_capitalizer

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_capitalizer)](https://github.com/oterrier/pyprocessors_capitalizer/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_capitalizer/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_capitalizer/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_capitalizer)](https://codecov.io/gh/oterrier/pyprocessors_capitalizer)
[![docs](https://img.shields.io/readthedocs/pyprocessors_capitalizer)](https://pyprocessors_capitalizer.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_capitalizer)](https://pypi.org/project/pyprocessors_capitalizer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_capitalizer)](https://pypi.org/project/pyprocessors_capitalizer/)

Processor based on Facebook's Capitalizer

## Installation

You can simply `pip install pyprocessors_capitalizer`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_capitalizer
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
