# pyprocessors_categories_from_annotations

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_categories_from_annotations)](https://github.com/oterrier/pyprocessors_categories_from_annotations/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_categories_from_annotations/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_categories_from_annotations/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_categories_from_annotations)](https://codecov.io/gh/oterrier/pyprocessors_categories_from_annotations)
[![docs](https://img.shields.io/readthedocs/pyprocessors_categories_from_annotations)](https://pyprocessors_categories_from_annotations.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_categories_from_annotations)](https://pypi.org/project/pyprocessors_categories_from_annotations/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_categories_from_annotations)](https://pypi.org/project/pyprocessors_categories_from_annotations/)

CategoriesFromAnnotations annotations coming from different annotators

## Installation

You can simply `pip install pyprocessors_categories_from_annotations`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_categories_from_annotations
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
