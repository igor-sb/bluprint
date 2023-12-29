Getting started with Bluprint
=============================

Python projects
---------------

To create a new directory *myproj* with the project template in the current directory, run:

.. code-block:: bash

    bluprint create myproj

This creates the following directory tree:

.. code-block:: none

  myproj
  ├── README.md
  ├── conf                            # yaml configuration files
  │   ├── config.yaml
  │   ├── data.yaml
  │   └── workflow.yaml
  ├── data                            # data such as csv, png, pdf
  │   └── example_data.csv
  ├── notebooks                       # jupyter notebooks
  │   └── example_jupyternb.ipynb
  ├── myproj                          # Python package of this project
  │   └── example.py
  └── pyproject.toml                  # Python package configuration

as well as:

* *.venv* directory with a Python virtual environment for this project
* *.gitignore* with files and file patterns excluded from version control (for example, *.env* often used to store secrets).

Allows notebooks to access Python files in *myproj* as modules with ``from myproj.example import add_one`` by installing the project as a Python package in the project's virtual environment.

Installs Python packages *bluprint_conf*, *ipykernel* and *pandas*.

Configuration
^^^^^^^^^^^^^

*conf* directory has three files that have a special meaning:

1. *config.yaml*: any general configuration

2. *data.yaml*: paths to local or remote data (tables, images, etc.)

3. *workflow.yaml*: workflow definitions for executing multiple notebooks



Accessing configuration
^^^^^^^^^^^^^^^^^^^^^^^

Access general configuration from *conf/config.yaml* files using:

.. code-block:: python

  from bluprint_conf import load_config_yaml

  cfg = load_config_yaml()

The first argument of ``load_config_yaml()`` has a default value ``conf/config.yaml`` so if you would like to load additional files or prefer a different name use:

.. code-block:: python

  cfg = load_config_yaml('conf/configuration.yaml')


Access data
^^^^^^^^^^^

Access files in the *data/* directory by first listing them in  using ``load_data_yaml()``


Python/R projects
-----------------

or if you would like to setup a Python/R project:

.. code-block:: bash

    bluprint create myproj -r

which also installs renv. To get started with RStudio, load the .Rproj file which also sets up project root directory as a working directory in R session.
