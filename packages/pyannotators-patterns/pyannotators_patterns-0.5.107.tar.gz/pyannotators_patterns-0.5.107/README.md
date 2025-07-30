# pyannotators_patterns

[![license](https://img.shields.io/github/license/oterrier/pyannotators_patterns)](https://github.com/oterrier/pyannotators_patterns/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyannotators_patterns/workflows/tests/badge.svg)](https://github.com/oterrier/pyannotators_patterns/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyannotators_patterns)](https://codecov.io/gh/oterrier/pyannotators_patterns)
[![docs](https://img.shields.io/readthedocs/pyannotators_patterns)](https://pyannotators_patterns.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyannotators_patterns)](https://pypi.org/project/pyannotators_patterns/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyannotators_patterns)](https://pypi.org/project/pyannotators_patterns/)

Annotator based on Facebook's Patterns

## Installation

You can simply `pip install pyannotators_patterns`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyannotators_patterns
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
