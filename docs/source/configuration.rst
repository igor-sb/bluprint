Project configuration
=====================

Bluprint project configuration is stored in yaml files within the project *conf* directory. Bluprint uses three types of yaml files for different purposes: *config.yaml*, *data.yaml* and *workflow.yaml*.

config.yaml
-----------

*config.yaml* is used to store any project configuration. This yaml file is loaded into an `OmegaConf dictionary <https://omegaconf.readthedocs.io/>`_ using ``load_config_yaml()`` function from the ``bluprint_conf`` package. OmegaConf dictionary behaves similar to a Python dictionary, but has extra functionality such as `variable interpolation <https://omegaconf.readthedocs.io/en/2.3_branch/usage.html#variable-interpolation>`_.

For example, this *conf/config.yaml*:

.. code-block:: yaml

  first:
    url: "www.google.com"
    port: 80
  second:
    url: "www.yahoo.com"
    port: 81

is used like this in a Python script or Jupyter notebook:

.. code-block:: python

    from bluprint_conf import load_config_yaml

    cfg = load_config_yaml()

    print(cfg.first)
    # {"url": "www.google.com", "port": 80}

    print(cfg.first.port)
    # 80


data.yaml
---------

*data.yaml* is used to store paths to various data files, from tables to images or other files. This file is loaded into a OmegaConf dictionary using ``load_data_yaml()`` from the ``bluprint_conf`` package. Paths in this file are either absolute or relative to the project's *data* directory. Relative paths are automatically parsed to obtain absolute paths in scripts or notebooks. 

workflow.yaml
-------------

*workflow.yaml* file contains definitions of notebook workflows (a list of notebooks to be exexcuted in series) in this format:

.. code-block:: yaml

  basic_workflow:
    - basic/preprocess.ipynb
    - basic/postprocess.ipynb
    - plot.Rmd

  other_workflow:
    - other/process.ipynb
    - plot.Rmd

Yaml keys are workflow names, and each element in a list contains a relative path to the notebook to be executed - relative to the project's *notebooks* directory. This example would reflect the following directory structure:

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

Once workflows are specified in this yaml file, they can be run in a shell using:

.. code-block:: shell

    bluprint workflow basic_workflow

This will run, in order:

1. *myproj/notebooks/basic/preprocess.ipynb*
2. *myproj/notebooks/basic/postprocess.ipynb*
3. *myproj/notebooks/plot.Rmd*
