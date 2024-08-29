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
  ├── .venv                           # Project's Python virtual environment
  ├── conf                            # Yaml configuration files
  │   ├── config.yaml                 #   Accessible using load_config_yaml()
  │   ├── data.yaml                   #   Accessible using load_data_yaml()
  │   └── workflow.yaml               #   Used by bluprint workflow
  ├── data                            # Local data (e.g. csv, png, pdf)
  │   └── example_data.csv
  ├── notebooks                       # Jupyter/R/Quarto notebooks
  │   ├── example_jupyternb.ipynb
  │   └── example_quarto.qmd
  ├── myproj                          # Python package of this project
  │   └── example.py                  #   Modules within myproj package
  ├── .gitignore                      # File list excluded from version control
  ├── README.md                       # Readme file describing the project
  ├── pyproject.toml                  # Project configuration
  └── uv.lock                         # Locked version of Python dependencies

and sets up the Python scripts in the *myproj* directory accessible as
``from myproj.example import add_one`` in any notebook or Python script that
uses this virtual environment and *bluprint_conf*.

*conf/config.yaml* contains this placeholder:

.. literalinclude:: ../../src/bluprint/template/conf/config.yaml
  :language: yaml

and *data/example_data.csv* contains:

.. literalinclude:: ../../src/bluprint/template/data/example_data.csv

Access data from *conf/data.yaml* and general configuration from
*conf/config.yaml* files using:

.. code-block:: python

  from bluprint_conf import load_data_yaml, load_config_yaml

  cfg = load_config_yaml()
  data = load_data_yaml()

  # Load `example_data.csv`:
  df = pd.read_csv(data.example_data)

  # Read configuration
  cfg.url   # "www.google.com"

By default, these functions load *conf/data.yaml* and *conf/config.yaml* so if
you have (additional) configuration in other files, specify them in the first
argument.

.. note::

  If you don't need to create various example files, you can create a project
  with:
  
  .. code-block::

    bluprint create myproject --omit-examples


Python/R projects
-----------------

Create a Bluprint project that supports both Jupyter and RMarkdown notebooks
with:

.. code-block:: bash

    bluprint create myproj -r

which also sets up renv and RStudio Rproj file and an example notebook:

.. code-block:: none

  myproj
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
  ├── renv                            # Project's R environment
  ├── .gitignore                      # Files excluded from version control
  ├── myproj.Rproj                    # Rproj file for RStudio projects
  └── pyproject.toml                  # Python package configuration

Python notebooks and code still work the same as in the Python-only project. R
notebooks and code can load the configuration and data using {reticulate} and
{here} packages that will be installed to the project's renv environment:

.. code-block:: r

  library(reticulate)
  use_python(here::here('.venv/bin/python'))
  bluprint_conf <- import('bluprint_conf')

  # Load `example_data.csv`:
  df <- bluprint_conf$load_data_yaml()

  cfg <- bluprint_conf$load_config_yaml()
  cfg$url  # "www.google.com"


Bluprint project in an existing directory
-----------------------------------------

If you already have an existing directory with data and notebooks, you can
initialize bluprint project using:

.. code-block:: bash

  bluprint init myproj

Check `bluprint init -h` for additional arguments. For example, if you want to
skip generating the example files:

.. code-block:: bash

  bluprint init myproj --omit-examples

.. code-block:: none

  myproj
  ├── .venv
  ├── conf
  │   └── data.yaml
  ├── data
  ├── notebooks
  ├── myproj
  ├── .gitignore
  ├── pyproject.toml
  └── README.md
