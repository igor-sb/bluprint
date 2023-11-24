"""Capture STDERR to string - used for unit testing."""

import sys
from io import StringIO


def capture_stderr(func, *args, **kwargs):
    buffer = StringIO()
    original_stderr = sys.stderr

    try:  # noqa: WPS501, WPS229
        sys.stderr = buffer
        func(*args, **kwargs)
        return buffer.getvalue()  # noqa: WPS331

    finally:
        sys.stderr = original_stderr
