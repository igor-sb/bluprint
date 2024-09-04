Project configuration
=====================

Bluprint project configuration is stored in *conf/\*.yaml* files, three of them
having special purposes: *config.yaml*, *data.yaml* and *workflow.yaml*.

config.yaml
-----------

*config.yaml* is used to store any project configuration in an arbitrary yaml
structure. This yaml file is loaded as an
`OmegaConf dictionary <https://omegaconf.readthedocs.io/>`_ using
``load_config_yaml()`` function. OmegaConf
dictionary behaves similar to a standard Python dictionary, but with extra
functionality such as `variable interpolation <https://omegaconf.readthedocs.io/en/2.3_branch/usage.html#variable-interpolation>`_.

For example, this *conf/config.yaml*:

.. code-block:: yaml

  first:
    url: "www.google.com"
    port: 80
  second:
    url: "www.yahoo.com"
    port: 81

can be loaded in a Python script or Jupyter notebook using:

.. code-block:: python

    from bluprint.config import load_config_yaml

    cfg = load_config_yaml()

    print(cfg.first)
    # {"url": "www.google.com", "port": 80}

    print(cfg.first.port)
    # 80


data.yaml
---------

*data.yaml* is used to store paths to files such as tables, images or plots, in
a yaml structure with arbitrary keys but where values are URIs, absolute paths
or paths relative to the *<project>/data/* directory. For example, this
project's *data/* directory:

.. code-block:: none

  myproj
  ├── conf
  │   ├── config.yaml
  │   └── data.yaml
  ├── data
  │   ├── raw
  │   │   └── user_data.csv
  │   ├── preprocessed
  │   │   └── user_data.csv
  │   ├── final
  │   │   └── user_data.csv
  │   └── metadata.csv
  ...

could be organized in the following *conf/data.yaml*:

.. code-block:: yaml

  user_data:
    raw: raw/user_data.csv
    preprocessed: preprocessed/user_data.csv
    final: raw/user_data.csv
  metadata: metadata.csv

Once loaded with ``load_data_yaml()``, these relative
paths are automatically parsed into absolute paths. Paths to other files that
are stored outside of the project directory, can be added into *data.yaml* and
will be loaded as-is. You can avoid duplicating the paths too, for example:

.. code-block:: yaml

  user_data:
    raw: raw/user_data.csv
    preprocessed: preprocessed/user_data.csv
    final: raw/user_data.csv
  metadata: metadata.csv

  paths:
    binaries: /long/absolute/path/to/your/binaries

  internal_binary1: ${paths.binaries}/local_binary1
  internal_binary2: ${paths.binaries}/local_binary2
  internal_binary3: ${paths.binaries}/local_binary3

  report: s3://path/to/final_report.ipynb

.. _config-workflows:

workflow.yaml
-------------

*workflow.yaml* file contains definitions of notebook workflows (a list of
notebooks to be exexcuted in series) in this format:

.. code-block:: yaml

  basic_workflow:
    - basic/preprocess.ipynb
    - basic/postprocess.ipynb
    - plot.Rmd

  other_workflow:
    - other/process.ipynb
    - plot.Rmd

Yaml keys are workflow names, and each element in a list contains a relative
path to the notebook to be executed - relative to the project's *notebooks*
directory. This example would reflect the following directory structure:

.. code-block:: none

  myproj
  ├── notebooks
  │   ├── basic
  │   │   ├── preprocess.ipynb
  │   │   └── postprocess.ipynb
  │   ├── other
  │   │   └── process.ipynb
  │   └── plot.Rmd
  ...

Once workflows are specified in this yaml file, they can be run in a shell
using:

.. code-block:: shell

    bluprint workflow basic_workflow

This will run, in order:

1. *myproj/notebooks/basic/preprocess.ipynb*
2. *myproj/notebooks/basic/postprocess.ipynb*
3. *myproj/notebooks/plot.Rmd*
