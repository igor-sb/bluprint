.. image:: images/bluprint_wide.png

Bluprint
========

Bluprint is a command line utility that helps organize exploratory data science
projects, which rely on "quick and dirty" analyses using notebooks.

Features
--------

* Project-specific Python/R environments

* Fully portable projects: copy or move the project folder anywhere

* Configuration and data paths organized in YAML files

* Project-specific code easily importable into notebooks:
  ``from myproject import function``

* Quickly check all notebook cells can be executed in order

* Setup simple notebook workflows through YAML


Installation
------------

.. code-block:: bash

   pipx install bluprint

This will make the bluprint available in any Python environment.


Requirements
------------

* `pyenv <https://github.com/pyenv/pyenv>`_: Python version manager

* `pipx <https://github.com/pypa/pipx>`_: Python package installer used for
  installing bluprint and poetry

* `poetry <https://python-poetry.org/docs/#installation>`_: Python package and
  dependency manager
   
* R packages {renv}, {reticulate}, {yaml} for RMarkdown notebooks

* Recommended: `rig <https://github.com/r-lib/rig>`_ to manage R versions





.. toctree::
   :maxdepth: 1
   :caption: Contents:

   tutorial
   configuration
   python_versions

.. toctree::
   :maxdepth: 1
   :caption: Existing projects:

   data_index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
