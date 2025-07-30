Open API Framework
==================

:Version: 0.12.0
:Source: https://github.com/maykinmedia/open-api-framework
:Keywords: metapackage, dependencies

|build-status| |code-quality| |ruff| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

A metapackage for registration components, that bundles the dependencies shared between these
components and provides generic base settings

.. contents::

.. section-numbering::

Features
========

* Bundling shared dependencies and introducing minimum versions for these dependencies
* Providing generic base Django settings to avoid duplicate settings across registration components

Usage
=====

Please see the hosted `documentation`_ for installation, configuration and usage instructions.

License
=======

Copyright © Maykin 2024

Licensed under the `MIT license`.


.. _`MIT license`: LICENSE


.. |build-status| image:: https://github.com/maykinmedia/open-api-framework/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/open-api-framework/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/maykinmedia/open-api-framework/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/open-api-framework/actions?query=workflow%3A%22Code+quality+checks%22

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. |coverage| image:: https://codecov.io/gh/maykinmedia/open-api-framework/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/open-api-framework
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/open-api-framework/badge/?version=latest
    :target: https://open-api-framework.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/open-api-framework.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/open-api-framework.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/open-api-framework.svg
    :target: https://pypi.org/project/open-api-framework/

.. _documentation: https://open-api-framework.readthedocs.io/en/latest/
