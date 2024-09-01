Custom template folders
=======================

You can create custom template folders and pass them as ``--template-dir``
argument to ``bluprint create``. Bluprint will copy the contents of this folder
to the new project. 

If files *README.md*, *notebooks/example_jupyter.ipynb* or
*notebooks/example_quarto.qmd* exits, any placeholder string
*{{placeholder_name}}* will be replaced with a project name.

If your *README.md* contains placeholder string *{{git_account_name}}*, it will
be replaced by your configured git username.
   
Template directory can contain anything. However, for Bluprint configs to work,
it needs a "conf" folder where Yaml configs will be stored and a "data" folder
where data will be stored, to which relative paths in *data.yaml* point to.

By default *bluprint_conf* function *load_config_yaml()* will look for
*conf/config.yaml* and *load_data_yaml()* will look for *conf/data.yaml*.
You can override these default names with the first argument of both functions.
Also, by default, *load_data_yaml()* will resolve relative paths relative to the
data folder in your project directory. This can be overriden too, e.g.
*load_data_yaml(data_dir='my_data')*.

Example
-------

If your template folder looks like this:

.. code::

    .
    ├── conf                          Yaml configuration files
    │   ├── config.yaml                 Accessible using load_config_yaml()
    │   ├── data.yaml                   Accessible using load_data_yaml()
    │   └── workflow.yaml               Used by bluprint workflow
    ├── data                          Will not overwrite existing data
    │   └── example_data.csv          Overwrites existing file unless --omit-examples
    ├── notebooks                     
    │   ├── example_jupyternb.ipynb   Overwrites existing file unless --omit-examples
    │   └── example_quarto.qmd        Overwrites existing file unless --omit-examples
    ├── myproj                        Python package of this project
    │   └── example.py                  Modules within myproj package
    ├── .gitignore                    Files excluded from version control
    ├── README.md                     Overwrites existing file unless --omit-examples
    └── pyproject.toml                Overwrites existing file

The files inside folders will tbe 