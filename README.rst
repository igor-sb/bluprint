.. image:: docs/source/images/bluprint_logo.png

Bluprint
========

**Bluprint** is a command line utility for streamlined exploratory data science projects. Bluprint allows seamless access to configuration, data and shared code in this type of project structure created by ``bluprint create my_project``::

    my_project
    ├── conf
    │   └── data.yaml
    ├── data
    │   ├── emailed
    │   │   └── messy.xlsx
    │   └── user_processed.csv
    ├── notebooks
    │   └── process.ipynb
    └── my_project
        └── shared_code.py

Storing paths relative to the *my_project* directory in *conf/data.yaml*:

.. code:: yaml

    emailed:
        messy: 'emailed/messy.xlsx'
    user:
        processed: 'user_processed.csv'

allows you access them in a Python script or Jupyter notebook anywhere within the project:

.. code:: python

    from bluprint_conf import load_data_yaml

    data = load_data_yaml() # By default loads conf/data.yaml
    print(data)
    #> {
    #>   'emailed': {
    #>     'messy': '/path/to/my_project/data/emailed/messy.xlsx'
    #>   },
    #>   'user': {
    #> 	   'processed': '/path/to/my_project/data/user_processed.csv'
    #>   },
    #>   'remote': {
    #>     'extras': 's3://path/to/extra_data.csv'
    #>   },
    #> }

    # Load data in a portable manner
    import pandas as pd
    messy_df = pd.read_xlsx(data.emailed.messy)
    extras_df = pd.read_xlsx(data.remote.extras)

    # Load shared code functions as Python modules
    from my_project.shared_code import transform_data
    transformed_df = transform_data(messy_df, extras_df)

    # Save output
    transformed_df.to_csv(data.user.processed)


.. note::

    For a working demonstration of a shareable project see https://github.com/igor-sb/bluprint-demo/.

Features
--------

- Write portable notebooks by loading configs with `load_data_yaml() <https://igor-sb.github.io/bluprint-conf/html/reference.html#bluprint_conf.data.load_data_yaml>`_ and `load_config_yaml() <https://igor-sb.github.io/bluprint-conf/html/reference.html#bluprint_conf.config.load_config_yaml>`_
- R/Python packages automatically version-locked using `renv <https://rstudio.github.io/renv/>`_ and `PDM <https://pdm-project.org/latest/>`_
- Import shared code as Python modules
- Install shared code across projects with `pip install <https://igor-sb.github.io/bluprint/prod_projects.html>`_
- Use both Python and R notebooks in a single project (see `Python/R projects </https://igor-sb.github.io/bluprint/getting_started.html#python-r-projects>`_)
- Share projects by copying a project directory and running *pdm install*
- Works with common IDEs (RStudio, VSCode), notebook tools for linting (`nbqa <https://nbqa.readthedocs.io/en/latest/>`_), notebook version control (`nbstripout <https://github.com/kynan/nbstripout>`_) or workflows (`Ploomber <https://github.com/ploomber/ploomber>`_)

Documentation
-------------

Full documentation available at: https://igor-sb.github.io/bluprint/.


Installation
------------

Install `pipx <https://github.com/pypa/pipx>`_ and `PDM <https://pdm-project.org/latest/>`_. Then run:

.. code:: shell

    pipx install bluprint

.. note::

    For R projects, install `renv <https://rstudio.github.io/renv/>`_ before attempting to create a Bluprint project with R support.

References
----------

Bluprint integrates:

* `PDM <https://pdm-project.org/latest/>`_
* `OmegaConf <https://omegaconf.readthedocs.io/>`_
* Python's native import system `importlib <https://docs.python.org/3/library/importlib.html>`_
* R packages `{renv} <https://rstudio.github.io/renv/>`_, `{here} <https://here.r-lib.org/>`_ and `{reticulate} <https://rstudio.github.io/reticulate/>`_

Bluprint is heavily inspired by these resources:

* Author's own frustration of dealing with malfunctioning notebooks for over a decade.
* `Cookiecutter Data Science <https://drivendata.github.io/cookiecutter-data-science/>`_
* `RStudio Projects <https://support.posit.co/hc/en-us/articles/200526207-Using-RStudio-Projects>`_
* `Ploomber <https://github.com/ploomber/ploomber>`_
* `Microsoft Team Data Science Process <https://learn.microsoft.com/en-us/azure/architecture/data-science-process/overview>`_
* `R for Data Science (2e): 6. Workflow: scripts and projects <https://r4ds.hadley.nz/workflow-scripts.html>`_
* `Vincent D. Warmerdam: Untitled12.ipynb | PyData Eindhoven 2019 <https://www.youtube.com/watch?v=yXGCKqo5cEY>`_

License
-------

Bluprint is released under `MIT license <LICENSE>`_.
