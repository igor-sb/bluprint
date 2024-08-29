.. image:: docs/source/images/bluprint_logo.png

Bluprint
========

.. |CI| image:: https://github.com/igor-sb/bluprint/actions/workflows/ci.yml/badge.svg
  :target: https://github.com/igor-sb/gencdna/actions

.. image:: https://codecov.io/gh/igor-sb/bluprint/graph/badge.svg?token=U44L2ASEIG 
 :target: https://codecov.io/gh/igor-sb/bluprint

**Bluprint** is a command line utility for creating data science project
templates, allowing R and Jupyter notebooks seamless access to configuration,
data and shared code in this type of structure::

    my_project
    ├── conf
    │   └── data.yaml              # YAML config with data paths
    ├── data                       # Store smaller data  
    │   ├── emailed
    │   │   └── messy.xlsx
    │   └── user_processed.csv
    ├── notebooks                  # Notebooks 
    │   └── process.ipynb
    └── my_project                 # Local Python package used by my_project
        └── shared_code.py

Configuration *conf/data.yaml* contains either absolute paths or paths relative
to the *my_project/data/*:

.. code:: yaml

    emailed:
        messy: 'emailed/messy.xlsx'
    user:
        processed: 'user_processed.csv'

This allows writing notebooks without hard-coding file paths, like this:

.. code:: python

    from bluprint_conf import load_data_yaml

    data = load_data_yaml()  # By default loads conf/data.yaml

    # Load data in a portable manner
    import pandas as pd
    messy_df = pd.read_xlsx(data.emailed.messy)
    extras_df = pd.read_xlsx(data.remote.extras)

    # Load shared code functions as Python modules
    # in any notebook anywhere in this project.
    from my_project.shared_code import transform_data
    transformed_df = transform_data(messy_df, extras_df)

    # Save output
    transformed_df.to_csv(data.user.processed)


.. note::

    For a working demonstration of a shareable project see
    https://github.com/igor-sb/bluprint-demo/.

Features
--------

- Write portable notebooks by storing all file paths to yaml configs and load
  them with `load_data_yaml() <https://igor-sb.github.io/bluprint-conf/html/reference.html#bluprint_conf.data.load_data_yaml>`_
  and `load_config_yaml() <https://igor-sb.github.io/bluprint-conf/html/reference.html#bluprint_conf.config.load_config_yaml>`_
- R/Python packages are version-locked with `renv <https://rstudio.github.io/renv/>`_
  and `uv <https://docs.astral.sh/uv/>`_
- Import packaged code as Python modules
- Packaged code can be shared across projects with `pip install <https://igor-sb.github.io/bluprint/prod_projects.html>`_
- Use both Python and R notebooks in a single project (see
  `Python/R projects </https://igor-sb.github.io/bluprint/getting_started.html#python-r-projects>`_)
- Share entire projects by copying a project directory and running
  *uv venv && uv sync*
- Works with common IDEs (RStudio, VSCode), notebook tools for linting (`nbqa <https://nbqa.readthedocs.io/en/latest/>`_),
  notebook version control (`nbstripout <https://github.com/kynan/nbstripout>`_)
  or workflows (`Ploomber <https://github.com/ploomber/ploomber>`_)

Documentation
-------------

Full documentation available at: https://igor-sb.github.io/bluprint/.


Installation
------------

Install Python 3.11.* (e.g. using `pyenv <https://github.com/pyenv/pyenv>`_)
and `uv <https://docs.astral.sh/uv/>`_. Then run:

.. code:: shell

    uv tool install bluprint

.. note::

    For R projects, install `renv <https://rstudio.github.io/renv/>`_ before
    attempting to create a Bluprint project with R support.

References
----------

Bluprint integrates:

* `uv <https://docs.astral.sh/uv/>`_
* `OmegaConf <https://omegaconf.readthedocs.io/>`_
* Python's native import system `importlib <https://docs.python.org/3/library/importlib.html>`_
* R packages `{renv} <https://rstudio.github.io/renv/>`_, `{here} <https://here.r-lib.org/>`_
  and `{reticulate} <https://rstudio.github.io/reticulate/>`_

Bluprint is inspired by these resources:

* `Cookiecutter Data Science <https://drivendata.github.io/cookiecutter-data-science/>`_
* `RStudio Projects <https://support.posit.co/hc/en-us/articles/200526207-Using-RStudio-Projects>`_
* `Ploomber <https://github.com/ploomber/ploomber>`_
* `Microsoft Team Data Science Process <https://learn.microsoft.com/en-us/azure/architecture/data-science-process/overview>`_
* `R for Data Science (2e): 6. Workflow: scripts and projects <https://r4ds.hadley.nz/workflow-scripts.html>`_
* `Vincent D. Warmerdam: Untitled12.ipynb | PyData Eindhoven 2019 <https://www.youtube.com/watch?v=yXGCKqo5cEY>`_

License
-------

Bluprint is released under `MIT license <LICENSE>`_.
