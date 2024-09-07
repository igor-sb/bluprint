Custom template folders
=======================

You can create custom template folders and pass them as ``--template-dir``
argument to ``bluprint create``. Bluprint will copy the contents of the template
folder to the new project and also do the following:

- If files *README.md*, *notebooks/example_jupyter.ipynb* or
  *notebooks/example_quarto.qmd* exits, any placeholder string
  *{{placeholder_name}}* will be replaced with a project name.

- If *README.md* contains placeholder string *{{git_account_name}}*, it will
   be replaced by git username.

- If there is *pyproject.toml* file, it will replace *{{placeholder_name}}* with
  project name and *{{python_version}}* with a Python version from the CLI
  argument.

Template directory can contain anything. However, for Bluprint configs to work,
it needs a folder to store yaml configs (default: *conf*) and another folder to
store data in the project to which relative paths in *data.yaml* point to
(default: *data*).

By default  *load_config_yaml()* looks for
*conf/config.yaml* and *load_data_yaml()* looks for *conf/data.yaml* in the
project folder. You can use different names and override these defaults;
for example this template folder::

    my_custom_template
    ├── configs
    │   ├── my_main_config.yaml
    │   └── my_data_config.yaml
    ├── my_data
    │   └── ...
    ├── {{placeholder_name}}
    │   └── my_code.py
    ├── README.md
    └── pyproject.toml

can be used to create a new project:

.. code:: bash

  bluprint create my_project --template-dir /path/to/my_custom_template


which can then be used:

.. code:: python

	from bluprint.config import load_config_yaml, load_data_yaml

	conf = load_config_yaml('configs/my_main_config.yaml')
	data = load_data_yaml('configs/my_data_config.yaml', data_dir='my_data')

This loads yaml configs from `configs` folder and parses locally stored data
from `my_data` in this project structure::

    my_project
    ├── configs
    │   ├── my_main_config.yaml
    │   └── my_data_config.yaml
    ├── my_data
    │   └── ...
    ├── my_project
    │   └── ...
    └── ...
