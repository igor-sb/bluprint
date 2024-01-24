Managing R versions
===================

Posit created a tool called `rig <https://github.com/r-lib/rig>`_ that is used to manage various versions of R (not its packages).

.. note::

  *rig* requires admin/sudo permissions.

After installing *rig*, available R versions can be viewed with:

.. code-block:: shell

  rig available
  # name   version  release date  type
  # ------------------------------------------
  # 3.0.3  3.0.3    2014-03-06    release
  # 3.1.3  3.1.3    2015-03-09    release
  # 3.2.5  3.2.5    2016-04-14    release
  # 3.3.3  3.3.3    2017-03-06    release
  # 3.4.4  3.4.4    2018-03-15    release
  # 3.5.3  3.5.3    2019-03-11    release
  # 3.6.3  3.6.3    2020-02-29    release
  # 4.0.5  4.0.5    2021-03-31    release
  # 4.1.3  4.1.3    2022-03-10    release
  # 4.2.3  4.2.3    2023-03-15    release
  # 4.3.2  4.3.2    2023-10-31    release
  # next   4.3.2                  patched
  # devel  4.4.0                  devel

Install another R version:

.. code-block:: shell

  rig add 4.3.2
  # [INFO] Running `sudo` for adding new R versions. This might need your password.
  # [sudo] password for igor:
  # [INFO] Downloading https://cdn.posit.co/r/ubuntu-2004/pkgs/r-4.3.2_1_amd64.deb -> /tmp/rig/r-4.3.2_1_amd64.deb
  # ...

Now a default R can be set with:

.. code-block:: shell

  rig default 4.3.2

  # Check the version:
  R --version
  # R version 4.3.2 (2023-10-31) -- "Eye Holes"
