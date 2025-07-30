========
Overview
========

Yet another Python library with helpers and utilities for data analysis and processing.

.. start-badges

| |version| |commits-since| |license|
| |supported-versions| |wheel| |downloads|
| |cicd| |coverage|

.. |version| image:: https://img.shields.io/pypi/v/jupyter-analysis-tools.svg
    :target: https://pypi.org/project/jupyter-analysis-tools
    :alt: PyPI Package latest release

.. |commits-since| image:: https://img.shields.io/github/commits-since/BAMresearch/jupyter-analysis-tools/v1.3.0.svg
    :target: https://github.com/BAMresearch/jupyter-analysis-tools/compare/v1.3.0...main
    :alt: Commits since latest release

.. |license| image:: https://img.shields.io/pypi/l/jupyter-analysis-tools.svg
    :target: https://en.wikipedia.org/wiki/MIT_license
    :alt: License

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/jupyter-analysis-tools.svg
    :target: https://pypi.org/project/jupyter-analysis-tools
    :alt: Supported versions

.. |wheel| image:: https://img.shields.io/pypi/wheel/jupyter-analysis-tools.svg
    :target: https://pypi.org/project/jupyter-analysis-tools#files
    :alt: PyPI Wheel

.. |downloads| image:: https://img.shields.io/pypi/dw/jupyter-analysis-tools.svg
    :target: https://pypi.org/project/jupyter-analysis-tools/
    :alt: Weekly PyPI downloads

.. |cicd| image:: https://github.com/BAMresearch/jupyter-analysis-tools/actions/workflows/ci-cd.yml/badge.svg
    :target: https://github.com/BAMresearch/jupyter-analysis-tools/actions/workflows/ci-cd.yml
    :alt: Continuous Integration and Deployment Status

.. |coverage| image:: https://img.shields.io/endpoint?url=https://BAMresearch.github.io/jupyter-analysis-tools/coverage-report/cov.json
    :target: https://BAMresearch.github.io/jupyter-analysis-tools/coverage-report/
    :alt: Coverage report

.. end-badges


Installation
============

::

    pip install jupyter-analysis-tools

You can also install the in-development version with::

    pip install git+https://github.com/BAMresearch/jupyter-analysis-tools.git@main


Documentation
=============

https://BAMresearch.github.io/jupyter-analysis-tools

Development
===========

Run all tests with::

    tox -e py

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
