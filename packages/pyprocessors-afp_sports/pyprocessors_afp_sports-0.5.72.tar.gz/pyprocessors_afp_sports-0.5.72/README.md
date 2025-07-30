# pyprocessors_afp_sports

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_afp_sports)](https://github.com/oterrier/pyprocessors_afp_sports/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_afp_sports/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_afp_sports/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_afp_sports)](https://codecov.io/gh/oterrier/pyprocessors_afp_sports)
[![docs](https://img.shields.io/readthedocs/pyprocessors_afp_sports)](https://pyprocessors_afp_sports.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_afp_sports)](https://pypi.org/project/pyprocessors_afp_sports/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_afp_sports)](https://pypi.org/project/pyprocessors_afp_sports/)

AFPSports annotations coming from different annotators

## Installation

You can simply `pip install pyprocessors_afp_sports`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_afp_sports
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
