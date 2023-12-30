Project configuration
=====================

Bluprint project configuration is stored in yaml files within the project *conf/* directory. There are three special yaml files that have a special purpose:

* config.yaml: This file is used to store generic project configuration and is loaded by default using ``load_config_yaml()`` function from ``bluprint_conf`` package.

* data.yaml: This file is used to store paths to various data files.

* workflow.yaml: This file defines notebook workflows, which are sequences of notebooks to be executed in a specific order.
