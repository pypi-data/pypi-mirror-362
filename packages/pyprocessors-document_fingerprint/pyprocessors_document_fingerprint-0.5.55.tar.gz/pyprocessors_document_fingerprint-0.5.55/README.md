# pyprocessors_document_fingerprint

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_document_fingerprint)](https://github.com/oterrier/pyprocessors_document_fingerprint/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_document_fingerprint/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_document_fingerprint/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_document_fingerprint)](https://codecov.io/gh/oterrier/pyprocessors_document_fingerprint)
[![docs](https://img.shields.io/readthedocs/pyprocessors_document_fingerprint)](https://pyprocessors_document_fingerprint.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_document_fingerprint)](https://pypi.org/project/pyprocessors_document_fingerprint/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_document_fingerprint)](https://pypi.org/project/pyprocessors_document_fingerprint/)

DocumentFingerprint annotations coming from different annotators

## Installation

You can simply `pip install pyprocessors_document_fingerprint`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_document_fingerprint
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
