# pysegmenters_rules_segmenter

[![license](https://img.shields.io/github/license/oterrier/pysegmenters_rules_segmenter)](https://github.com/oterrier/pysegmenters_rules_segmenter/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pysegmenters_rules_segmenter/workflows/tests/badge.svg)](https://github.com/oterrier/pysegmenters_rules_segmenter/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pysegmenters_rules_segmenter)](https://codecov.io/gh/oterrier/pysegmenters_rules_segmenter)
[![docs](https://img.shields.io/readthedocs/pysegmenters_rules_segmenter)](https://pysegmenters_rules_segmenter.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pysegmenters_rules_segmenter)](https://pypi.org/project/pysegmenters_rules_segmenter/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysegmenters_rules_segmenter)](https://pypi.org/project/pysegmenters_rules_segmenter/)

Rule based segmenter based on Spacy

## Installation

You can simply `pip install pysegmenters_rules_segmenter`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pysegmenters_rules_segmenter
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
