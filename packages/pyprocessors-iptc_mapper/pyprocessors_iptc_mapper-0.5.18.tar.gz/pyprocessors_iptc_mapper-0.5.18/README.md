# pyprocessors_iptc_mapper

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_iptc_mapper)](https://github.com/oterrier/pyprocessors_iptc_mapper/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_iptc_mapper/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_iptc_mapper/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_iptc_mapper)](https://codecov.io/gh/oterrier/pyprocessors_iptc_mapper)
[![docs](https://img.shields.io/readthedocs/pyprocessors_iptc_mapper)](https://pyprocessors_iptc_mapper.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_iptc_mapper)](https://pypi.org/project/pyprocessors_iptc_mapper/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_iptc_mapper)](https://pypi.org/project/pyprocessors_iptc_mapper/)

CategoriesFromAnnotations annotations coming from different annotators

## Installation

You can simply `pip install pyprocessors_iptc_mapper`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_iptc_mapper
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
