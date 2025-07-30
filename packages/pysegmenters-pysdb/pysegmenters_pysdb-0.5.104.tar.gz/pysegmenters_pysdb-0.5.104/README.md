# pysegmenters_pysdb

[![license](https://img.shields.io/github/license/oterrier/pysegmenters_pysdb)](https://github.com/oterrier/pysegmenters_pysdb/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pysegmenters_pysdb/workflows/tests/badge.svg)](https://github.com/oterrier/pysegmenters_pysdb/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pysegmenters_pysdb)](https://codecov.io/gh/oterrier/pysegmenters_pysdb)
[![docs](https://img.shields.io/readthedocs/pysegmenters_pysdb)](https://pysegmenters_pysdb.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pysegmenters_pysdb)](https://pypi.org/project/pysegmenters_pysdb/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysegmenters_pysdb)](https://pypi.org/project/pysegmenters_pysdb/)

Rule based segmenter based on Spacy

## Installation

You can simply `pip install pysegmenters_pysdb`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pysegmenters_pysdb
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
