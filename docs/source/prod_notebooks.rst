Production-grade notebooks
==========================

This page summarizes some of the external tools for productionizing Jupyter notebooks - and can be run easily within bluprint projects.

Version control
---------------

We can omit certain metadata, such as cell timestamps and execution counts, or cell output in Jupyter notebooks for the purposes of version control using `nbstripout <https://github.com/kynan/nbstripout>`_. To install `nbstripout` package in your project, run this one-time setup:

.. code-block:: bash

  pdm add nbstripout

and then install a git filter:

.. code-block:: bash

  pdm run nbstripout --install

Adding the ``--keep-output`` argument to the last command will keep cell output under version control. For more details see nbstripout `instructions <https://github.com/kynan/nbstripout>`_. After this, you can commit notebooks as usual in your project.


Best coding practices
---------------------

Install `nbqa <https://nbqa.readthedocs.io/en/latest/>`_ with:

.. code-block:: bash

  pdm add 'nbqa[toolchain]'

``nbqa`` allows you to use tools usually used for Python package development in
Jupyter notebooks. There are several tools worth mentioning that can help write
production-grade code in notebooks.

Linting
^^^^^^^

Flake8 is a linter, which is tool used to analyze and detect potential errors, bugs, and code style violations. To run flake8 on a ``notebooks/example_jupyter.ipynb`` notebook, run:

.. code-block:: bash

  pdm run nbqa flake8 notebooks/example_jupyter.ipynb

You can check the details of each of the violations on
`wemake-python-styleguide <https://wemake-python-styleguide.readthedocs.io/en/latest/pages/usage/violations/best_practices.html>`_ by using the search box on the left.

There are few ways to ignore violations:

1. Ignoring them in one specific line (for example for WPS221 violation), use:

   .. code-block:: python

     <python code that violates WPS211>  # noqa: WPS221

2. Ignoring them across the entire file; to achieve this add the following to ``pyproject.toml``:

   .. code-block:: toml

     [tool.flake8]
     per-file-ignores = ['notebooks/example_jupyter.ipynb: WPS211']

3. Ignoring them in the entire project; for this add this to ``pyproject.toml``:

   .. code-block:: toml

     [tool.flake8]
     ignore = ['WPS211']

For more details check the `flake8 documentation <https://flake8.pycqa.org/en/latest/>`_.

.. note::

  Flake8 imposes a very strict set of rules that most authors do not follow to the letter - keep this in mind - more over with notebooks. However, it is still a valuable tool that can be used to write better code and preventing the need to rewrite the notebook code in separate Python scripts / packages.

Sorting imports
^^^^^^^^^^^^^^^

Since notebooks tend to have a lot of functions, objects or modules imported, I recommend using `isort <https://pycqa.github.io/isort/>`_ to automatically sort your imports and group them into sections:

.. code-block:: bash

  pdm run nbqa isort notebooks/example_jupyternb.ipynb

This will update your notebook in-place.

Python scripts
^^^^^^^^^^^^^^

You can run flake8, isort, etc. on Python scripts as well, just omit ``nbqa`` from commands above. For example, to run a flake8 linter:

.. code-block:: bash

  pdm run flake8 project_name/example.py

Testing
-------

Notebooks can be tested by ensuring all cells execute without an error, when ran in the order in which they appear. For this purpose, ``bluprint notebook`` can be used to run a notebook:

.. code-block:: bash

  bluprint notebook notebooks/example_jupyternb.ipynb

Notebook workflows can be tested by specifying yaml workflow file, e.g. ``workflow.yaml``, naming a workflow (e.g. ``example_workflow``) then running:

.. code-block:: bash

  blurpint workflow example_workflow \
    --workflow_yaml=example_workflow \
    --notebook_dir=notebooks

For Jupyter notebook workflows with more features, check `ploomber <https://docs.ploomber.io/en/latest/get-started/what-is.html>`_.