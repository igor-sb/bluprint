.. image:: docs/source/images/bluprint_logo.png

Bluprint
========

**Bluprint** is a command line utility for streamlined exploratory data science projects. Bluprint projects allow Jupyter and RMarkdown notebooks seamless access to configuration, data and shared code, using best coding practices, in this type of project structure::

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


Features
--------

* Configuration, data and shared code (Python/R scripts) separated from notebooks.

* Mixing of any or all Python/R scripts and Jupyter/RMarkdown notebooks.

* Consistent access to configuration and data, e.g. ``data.emailed.messy`` (Python) automatically resolves to */path/to/my_project/data/emailed/messy.xlsx*.

* Consistent access to project modules, e.g. ``from my_project import shared_code`` in any notebook in any sub-directory.

* Share project easily; just copy the project directory and run ``pdm install``.

* Reproducibility: Python and R dependencies are version locked.

* Works with tools for notebook linting, testing, CI/CD and workflows.

* Bluprint projects are Python packages; use ``pip install /path/to/my_project`` to reuse shared code across projects.


Usage
-----

``bluprint create my_project`` creates a project skeleton similar to the example shown above. Once created, we can add data files and store all file paths relative to the *my_project/data* directory, in the *data.yaml*:

.. code:: yaml

    emailed:
        messy: 'emailed/messy.xlsx'
    user:
        processed: 'user_processed.csv'

Then retrieve the automatically parsed full paths, for example in *process.ipynb* above:

.. code:: python

    # bluprint_conf is a helper package for loading configs 
    from bluprint_conf import load_data_yaml
    from my_project.shared_code import process_data
    import pandas as pd

    data = load_data_yaml() # default arg: conf/data.yaml
    print(data)
    #> {
    #>   'emailed': {
    #>     'messy': '/path/to/my_project/data/emailed/messy.xlsx'
    #>   },
    #>   'user': {
    #> 	   'processed': '/path/to/my_project/data/user_processed.csv'
    #>   }
    #> }

    messy_df = pd.read_xlsx(data.emailed.messy)

    processed_df = process_data(messy_df)

    processed_df.to_csv(data.user.processed)

For a working demonstration of a shareable project https://github.com/igor-sb/bluprint-demo/.

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
* Python's native import system
* R package `renv <https://rstudio.github.io/renv/>`_
* R package `here <https://here.r-lib.org/>`_ 
* R package `reticulate <https://rstudio.github.io/reticulate/>`_

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
