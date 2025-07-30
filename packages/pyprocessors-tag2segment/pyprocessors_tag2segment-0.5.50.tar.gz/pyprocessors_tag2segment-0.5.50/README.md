# pyprocessors_tag2segment

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_tag2segment)](https://github.com/oterrier/pyprocessors_tag2segment/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_tag2segment/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_tag2segment/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_tag2segment)](https://codecov.io/gh/oterrier/pyprocessors_tag2segment)
[![docs](https://img.shields.io/readthedocs/pyprocessors_tag2segment)](https://pyprocessors_tag2segment.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_tag2segment)](https://pypi.org/project/pyprocessors_tag2segment/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_tag2segment)](https://pypi.org/project/pyprocessors_tag2segment/)

Create segments from annotations

## Installation

You can simply `pip install pyprocessors_tag2segment`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_tag2segment
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
