# pyconverters_xcago

[![license](https://img.shields.io/github/license/oterrier/pyconverters_xcago)](https://github.com/oterrier/pyconverters_xcago/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyconverters_xcago/workflows/tests/badge.svg)](https://github.com/oterrier/pyconverters_xcago/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyconverters_xcago)](https://codecov.io/gh/oterrier/pyconverters_xcago)
[![docs](https://img.shields.io/readthedocs/pyconverters_xcago)](https://pyconverters_xcago.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyconverters_xcago)](https://pypi.org/project/pyconverters_xcago/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyconverters_xcago)](https://pypi.org/project/pyconverters_xcago/)

Fetch articles from Pubmed

## Installation

You can simply `pip install pyconverters_xcago`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyconverters_xcago
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
