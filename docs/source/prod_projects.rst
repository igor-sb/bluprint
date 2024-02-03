Sharing projects
================

Bluprint projects can be shared and reused directly out-of-the-box. You can push or pull bluprint projects from Github or even just copy and paste them into a directory of your choice. To run notebooks and code from a bluprint project, you only need `PDM <https://pdm-project.org/latest/>`_ 

.. note:

  Existing bluprint projects can be run without ``bluprint``. 

For example, you can download and test the demo project:

.. code-block:: bash

	git clone https://github.com/igor-sb/bluprint-demo.git
	cd bluprint-demo
	pdm install

This will clone the demo project, install all necessary dependencies and setup the Python/R environments to be identical to the ones from a creator of the project.

Bluprint can be used to package and store your projects on Github, so that code outside of notebooks can be reused by other people. Projects can be shared by pushing them to Github or simply copying the 
