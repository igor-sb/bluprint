Managing Python versions
========================

You can use `pyenv <https://github.com/pyenv/pyenv#installation>`_ to manage
Python versions. Once it is installed, use ``pyenv versions`` to see which
Python versions are installed:

.. code-block:: bash

	pyenv versions
	# system
	# 3.9.8
	# 3.10.10
	# * 3.11.2 (set by /home/igor/repos/.python-version)
	# 3.12.0
	# 3.12.0a5
	# 3.13.0a2

Here's how to get Python versions available to download and install:

.. code-block:: bash

	pyenv install -l | grep '\s[0-9]'
	# ...
	# 3.11.2
	# 3.11.3
	# 3.11.4
	# 3.11.5
	# 3.11.6
	# 3.12.0
	# 3.12-dev
	# 3.13.0a2
	# 3.13-dev

Installing a new version, e.g. 3.13.0a2:

.. code-block:: bash

	pyenv install 3.13.0a2
	# Downloading Python-3.13.0a2.tar.xz...
	# -> https://www.python.org/ftp/python/3.13.0/Python-3.13.0a2.tar.xz
	# Installing Python-3.13.0a2...
	# Installed Python-3.13.0a2 to /home/igor/.pyenv/versions/3.13.0a2


Once a different Python version is install you can use it

* globally using: ``pyenv global 3.13.0a2``

* locally (whenever you are in the current directory) using ``pyenv local 3.13.0a2``

.. note::

	pyenv works on Linux, MacOS and Windows Subsystem for Linux. For native Windows consider `pyenv-win <https://github.com/pyenv-win/pyenv-win>`_.
