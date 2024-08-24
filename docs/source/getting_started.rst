Getting started
===============

Python projects
---------------

Create a project template in a new directory *myproj* using:

.. code-block:: bash

    bluprint create myproj

This creates the following directory tree:

.. code-block:: none

  myproj
  ├── conf
  │   ├── config.yaml
  │   ├── data.yaml
  │   └── workflows.yaml
  ├── data
  │   └── example_data.csv
  ├── notebooks
  │   ├── example_jupyternb.ipynb
  │   └── example_quarto.qmd
  ├── myproj
  │   ├── __init__.py
  │   └── example.py
  ├── README.md
  └── pyproject.toml

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

It also creates a Python virtual environment in the *.venv* directory, sets up the Python files in the *myproj* directory accessible as ``from myproj.example import add_one`` in any notebook or Python script that uses this virtual environment and installs Python packages *bluprint_conf*, *ipykernel* and *pandas*.

By default *conf/config.yaml* contains this placeholder:

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

which also sets up renv and RStudio Rproj file and an example notebook:

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
  ├── notebooks                       # Jupyter and RMarkdown notebooks
  │   ├── example_jupyternb.ipynb
  │   └── example_rmarkdown.Rmd
  ├── myproj                          # Python package of this project
  │   └── example.py
  ├── myproj.Rproj                    # Rproj file for RStudio projects
  ├── renv                            # Project's R environment
  └── pyproject.toml                  # Python package configuration

Python notebooks and code still work the same as in the Python-only project. R notebooks and code can load the configuration and data using {reticulate} and {here} packages that are pre-installed to the project's renv:

.. code-block:: r

  library(reticulate)
  use_python(here::here('.venv/bin/python'))
  bluprint_conf <- import('bluprint_conf')

  # Load `example_data.csv`:
  df <- bluprint_conf$load_data_yaml()

  cfg <- bluprint_conf$load_config_yaml()
  cfg$url  # "www.google.com"
