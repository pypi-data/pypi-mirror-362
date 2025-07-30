# pyannotators_spacyner

[![license](https://img.shields.io/github/license/oterrier/pyannotators_spacyner)](https://github.com/oterrier/pyannotators_spacyner/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyannotators_spacyner/workflows/tests/badge.svg)](https://github.com/oterrier/pyannotators_spacyner/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyannotators_spacyner)](https://codecov.io/gh/oterrier/pyannotators_spacyner)
[![docs](https://img.shields.io/readthedocs/pyannotators_spacyner)](https://pyannotators_spacyner.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyannotators_spacyner)](https://pypi.org/project/pyannotators_spacyner/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyannotators_spacyner)](https://pypi.org/project/pyannotators_spacyner/)

Annotator based on Facebook's SpacyNER

## Installation

You can simply `pip install pyannotators_spacyner`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyannotators_spacyner
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
