Data index
==========

``bluprint index`` creates a YAML configuration file from a directory of data
files. For example, ``bluprint index data data.yaml`` parses the following
``data`` directory::

	data
	├── dir1
	│   ├── dir1a
	│   │   ├── file1.txt
	│   │   └── file2.txt
	│   └── file3.txt
	├── dir2
	│   └── file4.txt
	└── file5.txt

into this ``data.yaml``:

.. code-block:: yaml

	dir1:
		dir1a:
			file1: dir1/dir1a/file1.txt
			file2: dir1/dir1a/file2.txt
		file3: dir1/file3.txt
	dir2:
		file4: dir2/file4.txt
	file5: file5.txt

This YAML file can then be updated manually as needed and then loaded into a
notebook. Then, we can access these filenames through YAML configuration keys
instead of dealing with various paths.
