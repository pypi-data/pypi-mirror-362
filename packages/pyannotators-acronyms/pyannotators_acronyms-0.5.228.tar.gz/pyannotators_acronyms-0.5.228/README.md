# pyannotators_acronyms

[![license](https://img.shields.io/github/license/oterrier/pyannotators_acronyms)](https://github.com/oterrier/pyannotators_acronyms/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyannotators_acronyms/workflows/tests/badge.svg)](https://github.com/oterrier/pyannotators_acronyms/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyannotators_acronyms)](https://codecov.io/gh/oterrier/pyannotators_acronyms)
[![docs](https://img.shields.io/readthedocs/pyannotators_acronyms)](https://pyannotators_acronyms.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyannotators_acronyms)](https://pypi.org/project/pyannotators_acronyms/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyannotators_acronyms)](https://pypi.org/project/pyannotators_acronyms/)

Annotator based on Facebook's Acronyms

## Installation

You can simply `pip install pyannotators_acronyms`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyannotators_acronyms
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
