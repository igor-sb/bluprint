Production-grade projects
=========================

There are a number of external tools that can be used to productionize your Jupyter notebooks. They can be run easily within bluprint projects.

Version control
---------------

It may be convenient to the changes in metadata, for example cell timestamps and execution counts, as well as cell outputs in notebooks for the purposes of version control. Python package `nbstripout <https://github.com/kynan/nbstripout>`_ can be used to automatically do this for version controlling Jupyter notebooks using ``git``.

To install `nbstripout` package in your project, run this one-time setup:

.. code-block:: bash

  pdm add nbstripout

instead of running ``pip install``. Then setup this special Jupyter notebook version control with:

.. code-block:: bash

  pdm run nbstripout --install

For more details see nbstripout `instructions <https://github.com/kynan/nbstripout>`_. After this, you can commit notebooks as usual in your project.


Writing quality code
--------------------

Install `nbqa <https://nbqa.readthedocs.io/en/latest/>`_ with:

.. code-block:: bash

  pdm add 'nbqa[toolchain]'

``nbqa`` allows you to use tools usually used for Python package development in
Jupyter notebooks. There are several tools worth mentioning that can help write
production-grade code in notebooks.

Linting
^^^^^^^

Flake8 is a linter, which is tool used to analyze and detect potential errors, bugs, and code style violations. To run flake8 on a ``notebooks/example_jupyter.ipynb`` notebook run:

.. code-block:: bash

  pdm run nbqa flake8 notebooks/example_jupyter.ipynb

You can check the details of each of the violations on
`wemake-python-styleguide <https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/best_practices.html>`_ by searching them in the search box on the left.

There are few ways to setup exceptions for exceptions. For example, for violating WPS221 exception, we can make flake8 ignore it one-time with this special comment:

.. code-block:: python

  <python code that violates WPS211>  # noqa: WPS221

Or add this to ``pyproject.toml`` in the root directory of your project:

.. code-block:: toml

  [tool.flake8]
  per-file-ignores = ['notebooks/example_jupyter.ipynb: WPS211']

Alternatively, we can ignore it for entire project by adding this to ``pyproject.toml``:

.. code-block:: toml

  [tool.flake8]
  ignore = ['WPS211']

For more details check the `flake8 documentation <https://flake8.pycqa.org/en/latest/>`_.

.. note::

  Flake8 imposes a very strict set of rules that most authors do not follow to
  the letter - keeop this in mind especially with notebooks. However, I would
  still highly encouring using it as a tool to teach you write better code
  and preventing the need to rewrite the notebook code in separate Python
  scripts / packages.

Sorting imports
^^^^^^^^^^^^^^^

Since notebooks tend to have a lot of functions, objects or modules imported, I recommend using `isort <https://pycqa.github.io/isort/>`_ to automatically sort your imports and group them into sections:

.. code-block:: bash

  pdm run nbqa isort notebooks/example_jupyternb.ipynb

This will update your notebook in-place.

QA on Python scripts
--------------------

You can run flake8, isort, etc. on Python scripts as well, just omit ``nbqa`` from commands above. For example, to run a flake8 linter:

.. code-block:: bash

  pdm run flake8 project_name/example.py

