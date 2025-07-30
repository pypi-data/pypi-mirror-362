# pyprocessors_bel_entities

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_bel_entities)](https://github.com/oterrier/pyprocessors_bel_entities/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_bel_entities/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_bel_entities/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_bel_entities)](https://codecov.io/gh/oterrier/pyprocessors_bel_entities)
[![docs](https://img.shields.io/readthedocs/pyprocessors_bel_entities)](https://pyprocessors_bel_entities.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_bel_entities)](https://pypi.org/project/pyprocessors_bel_entities/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_bel_entities)](https://pypi.org/project/pyprocessors_bel_entities/)

BELEntities annotations coming from different annotators

## Installation

You can simply `pip install pyprocessors_bel_entities`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_bel_entities
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
