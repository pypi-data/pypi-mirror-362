# pyprocessors_segment_renseignor

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_segment_renseignor)](https://github.com/oterrier/pyprocessors_segment_renseignor/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_segment_renseignor/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_segment_renseignor/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_segment_renseignor)](https://codecov.io/gh/oterrier/pyprocessors_segment_renseignor)
[![docs](https://img.shields.io/readthedocs/pyprocessors_segment_renseignor)](https://pyprocessors_segment_renseignor.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_segment_renseignor)](https://pypi.org/project/pyprocessors_segment_renseignor/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_segment_renseignor)](https://pypi.org/project/pyprocessors_segment_renseignor/)

Create segments from annotations

## Installation

You can simply `pip install pyprocessors_segment_renseignor`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_segment_renseignor
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
