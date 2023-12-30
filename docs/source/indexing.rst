Indexing existing data
======================

In pre-existing projects, you may already have a *data* directory populated with various files and organized in different subdirectories. Instead of manually writing down all file paths in a *conf/data.yaml*, you can use:

.. code-block:: shell

    bluprint index data conf/data.yaml

which recursively indexes a *data/* directory in your current path and saves the output into *conf/data.yaml*. For example, if the data directory has the following structure::

    data
    ├── dir1
    │   ├── dir1a
    │   │   ├── file_1.txt
    │   │   ├── file.1.txt
    │   │   └── file2.txt
    │   ├── .skipme
    │   └── file3.txt
    ├── dir2
    │   └── file4.txt
    └── file5.txt

*conf/data.yaml* will look like this:

.. code-block:: yaml

    dir1:
        dir1a:
            file_1: dir1/dir1a/file.1.txt
            file2: dir1/dir1a/file2.txt
            file_1_txt: dir1/dir1a/file_1.txt
        file3: dir1/file3.txt
    dir2:
        file4: dir2/file4.txt
    file5: file5.txt

with paths listed relative to the *data/* directory.

.. note::

    By default, ``bluprint index`` will omit any files starting with a dot. Use ``--skip_dot_files False`` argument to index dot files as well.
