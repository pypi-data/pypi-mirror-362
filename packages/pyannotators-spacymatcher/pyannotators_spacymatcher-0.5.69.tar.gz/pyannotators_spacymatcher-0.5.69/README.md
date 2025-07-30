# pyannotators_spacymatcher

[![license](https://img.shields.io/github/license/oterrier/pyannotators_spacymatcher)](https://github.com/oterrier/pyannotators_spacymatcher/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyannotators_spacymatcher/workflows/tests/badge.svg)](https://github.com/oterrier/pyannotators_spacymatcher/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyannotators_spacymatcher)](https://codecov.io/gh/oterrier/pyannotators_spacymatcher)
[![docs](https://img.shields.io/readthedocs/pyannotators_spacymatcher)](https://pyannotators_spacymatcher.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyannotators_spacymatcher)](https://pypi.org/project/pyannotators_spacymatcher/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyannotators_spacymatcher)](https://pypi.org/project/pyannotators_spacymatcher/)

Annotator based on Facebook's SpacyMatcher

## Installation

You can simply `pip install pyannotators_spacymatcher`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyannotators_spacymatcher
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
