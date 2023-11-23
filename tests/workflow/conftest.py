"""Test fixtures."""

import os
from pathlib import Path

base_path = os.path.abspath('.')
fixture_path = Path(base_path) / 'tests' / 'workflow' / 'fixtures'
