Getting started with Bluprint
=============================

Python projects
---------------

Create a project template in a new directory *myproj* using:

.. code-block:: bash

    bluprint create myproj

This creates the following directory tree:

.. code-block:: none

  myproj
  ├── .gitignore                      # Files excluded from version control
  ├── .venv                           # Project's Python virtual environment
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

It also creates a Python virtual environment in the *.venv* directory, sets up the Python files in the *myproj* directory accessible as ``from myproj.example import add_one`` in any notebook or Python script that uses this virtual environment and installs Python packages *bluprint_conf*, *ipykernel* and *pandas* in this virtual environment.

By default *conf/config.yaml* contains:

.. literalinclude:: ../../src/bluprint/template/conf/config.yaml
  :language: yaml

and *data/example_data.csv* contains:

.. literalinclude:: ../../src/bluprint/template/data/example_data.csv

Access data from *conf/data.yaml* and general configuration from *conf/config.yaml* files using:

.. code-block:: python

  from bluprint_conf import load_data_yaml, load_config_yaml

  cfg = load_config_yaml()
  data = load_data_yaml()

  # Load `example_data.csv`:
  df = pd.read_csv(data.example_data)

  # Read configuration
  cfg.url   # "www.google.com"

By default, these functions load *conf/data.yaml* and *conf/config.yaml* so if you have (additional) configuration in other files, specify them in the first argument.


Python/R projects
-----------------

If you would like to setup a Python/R project that supports both Jupyter and RMarkdown notebooks use:

.. code-block:: bash

    bluprint create myproj -r

which also installs renv:

.. code-block:: none

  myproj
  ├── .gitignore                      # Files excluded from version control
  ├── .venv                           # Project's Python virtual environment
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

To get started with RStudio, load the .Rproj file which also sets up project root directory as a working directory in R session.
