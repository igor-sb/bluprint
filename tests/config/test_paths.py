"""Tests for package paths."""

from pathlib import Path

from bluprint.config import absolute_path_in_project


def test_absolute_path_in_project():
    assert absolute_path_in_project('tests') == Path.cwd() / 'tests'
