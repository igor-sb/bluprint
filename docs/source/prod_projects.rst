Sharing projects
================

Bluprint projects can be shared and reused directly out-of-the-box. Simply copy the project folder (or pull from Github) and run ``pdm install``. The only pre-requisite is having `PDM <https://pdm-project.org/latest/>`_ installed.

.. note:

  Existing bluprint projects can be run without ``bluprint``. 

For example, to download and test the demo project:

.. code-block:: bash

	git clone https://github.com/igor-sb/bluprint-demo.git
	cd bluprint-demo
	pdm install

This will clone the demo project, install all necessary dependencies and setup the Python/R environments to be identical to the ones from a creator of the project.

Bluprint can be used to package and store your projects on Github, so that Python code outside of notebooks can be reused by other people. For example, if you want to reuse a Python code from a project ``my_project``, which lives in */path/to/my_project* in a new project */path/to/new_project*, run this from */path/to/new_project*:

.. code-block:: bash

	pdm add /path/to/my_project
	# or if you prefer pip / manage virtual env. yourself:
	pip install /path/to/my_project
