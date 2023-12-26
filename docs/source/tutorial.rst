Getting started with bluprint
=============================

Python projects
---------------

Create a new directory *myproj* with the project template:

.. code-block:: bash

    bluprint create myproj

This command:

1. Creates the following directory tree::

    myproj
    ├── README.md
    ├── conf
    │   ├── config.yaml
    │   ├── data.yaml
    │   └── workflow.yaml
    ├── data
    │   └── example_data.csv
    ├── notebooks
    │   └── example_jupyternb.ipynb
    ├── myproj
    │   └── example.py
    └── pyproject.toml

  as well as:

  * *.venv* directory with Python virtual environment for this project
  * *.gitignore* with reasonable defaults - for example *.env* where secrets may be stored in plain text

2. Installs the project as an "editable" Python package. This allows notebooks to access Python files in *myproj* as modules with ``from myproj.example import add_one``.

3. Installs Python packages *bluprint_conf*, *ipykernel* and *pandas*.

*conf* directory has three files that have a special meaning:

  1. *config.yaml*: any general configuration
  2. *data.yaml*: paths to local or remote data (tables, images, etc.)
  3. *workflow.yaml*: workflow definitions for executing multiple notebooks

*data*: place to store local data in any hierarchy
*notebooks*: place to store notebooks in any hierarchy
*myproj*: Python modules that can be loaded into notebooks



Python/R projects
-----------------

or if you would like to setup a Python/R project:

.. code-block:: bash

    bluprint create myproj -r

which also installs renv. To get started with RStudio, load the .Rproj file which also sets up project root directory as a working directory in R session.
