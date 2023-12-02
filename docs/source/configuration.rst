Project configuration
=====================

Bluprint project configuration is stored as YAML files within the project
 ``conf``. There are three special yaml files that have a special purpose:

* config.yaml: This file stores generic project configuration and is loaded automatically
using bluprint's `load_config_yaml()` function.

* data.yaml: data.yaml is the main configuration file 

* workflow.yaml: This file defines notebook workflows, which are sequences of notebooks to be
executed in a specific order. 

