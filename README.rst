.. image:: docs/source/images/bluprint_logo.png

Bluprint
========

**Bluprint** is a command line utility for streamlining exploratory data science projects using Jupyter and RMarkdown notebooks. Bluprint projects allow notebooks seamless access to configuration, data and shared code across directories in this type of structure::

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
        └── common_code.py

Bluprint integrates `PDM <https://pdm-project.org/latest/>`_, `OmegaConf <https://omegaconf.readthedocs.io/>`_, Python's native import system and R packages `renv <https://rstudio.github.io/renv/>`_, `here <https://here.r-lib.org/>`_ and `reticulate <https://rstudio.github.io/reticulate/>`_ to allow the use of good coding practices in both Python and R notebooks:

* File paths are easily accessible in Python dictionaries or R's named lists.

* Configuration (*conf/*), data (*data/*) and shared code separated from notebooks.

* Exploratory projects can be easily shared; for example see `demo project <https://github.com/igor-sb/bluprint-demo/>`_.

* Mix and match Python, R, Jupyter and RMarkdown.

* Better reproducibility by version-locking Python and R dependencies.

* Notebook workflows help catch potential errors when all cells are run in order.


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

    from bluprint_conf import load_data_yaml
    from my_project.common_code import process_data
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

Installation
------------

Install `pipx <https://github.com/pypa/pipx>`_ and `PDM <https://pdm-project.org/latest/>`_. Then run:

.. code:: shell

    pipx install bluprint


License
-------

Bluprint is released under `MIT license <LICENSE>`_.
