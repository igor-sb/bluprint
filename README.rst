.. image:: docs/source/images/bluprint_logo.png

Bluprint
========

Bluprint is a command line utility for organizing exploratory data science projects in a cookiecutter-type directory structure.

.. grid:: 2

    .. grid-item::

        Project structure::

            demo
            ├── conf
            │   └── data.yaml
            ├── data
            │   ├── emailed
            │   │   └── messy.xlsx
            │   └── user_processed.csv
            ├── notebooks
            │   ├── pre
            │   │   └── process.ipynb
            │   └── final_report.ipynb
            └── demo
                └── common_code.py

    .. grid-item::

        File paths are listed relative to the *demo/data* directory and stored in the ``data.yaml``:

        .. code:: yaml

            emailed:
            - messy: 'emailed/messy.xlsx'
            user:
            - processed: 'user_processed.csv'





Bluprint also installs the entire directory as an editable Python package (like `Cookiecutter Data Science <https://drivendata.github.io/cookiecutter-data-science/>`_, which means Python source code can be easily imported into notebooks.

Here's an example of how *process.ipynb* could look:

.. code:: python

    from bluprint_conf import load_data_yaml
    from demo.common_code import process_data
    import pandas as pd

    data = load_data_yaml() # default arg: conf/data.yaml
    print(data)
    #> {
    #>   'emailed': {
    #>     'messy': '/path/to/demo/data/emailed/messy.xlsx'
    #>   },
    #>   'user': {
    #> 	   'processed': '/path/to/demo/data/user_processed.csv'
    #>   }
    #> }

    messy_df = pd.read_xlsx(data.emailed.messy)

    processed_df = process_data(messy_df)

    processed_df.to_csv(data.user.processed)

For a demonstration of a shareable project https://github.com/igor-sb/bluprint-demo/ .

Features
--------

* No more copy/pasting file paths across notebooks.

* Configuration, data and shared code separated from notebooks.

* `OmegaConf <https://omegaconf.readthedocs.io/>`_ configurations support `variable interpolation <https://omegaconf.readthedocs.io/en/2.3_branch/usage.html#variable-interpolation>`_ and `merging multiple yaml files <https://omegaconf.readthedocs.io/en/2.3_branch/usage.html#merging-configurations>`_ into a single config object.

* Reproducible and shareable exploratory projects (`example <https://github.com/igor-sb/bluprint-demo/>`_).

* Mix and match Python, R, Jupyter and RMarkdown notebooks.

* Support for simple notebook workflows.


Installation
------------

Install `pipx <https://github.com/pypa/pipx>`_ and `PDM <https://pdm-project.org/latest/>`_. Then run:

.. code:: shell

    pipx install bluprint


---

Bluprint is released under `MIT license <LICENSE>`_.
