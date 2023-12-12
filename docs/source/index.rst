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

* `pipx <https://github.com/pypa/pipx>`_: Python package installer used for
  installing bluprint

* `pdm <https://pdm-project.org/latest/>`_: Python dependency manager
   
* For RMarkdown notebooks R packages {renv}, {reticulate} and {yaml}

Recommended:

* `pyenv <https://github.com/pyenv/pyenv>`_ to manage Python versions
* `rig <https://github.com/r-lib/rig>`_ to manage R versions







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
