"""Test Python version defaults."""

from bluprint.create.py_project import default_python_version


def test_too_low_default_python():
    assert default_python_version(min_version='999.999') == '999.999'
