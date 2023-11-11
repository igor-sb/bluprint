"""Wrapper for binary executables."""

from dataclasses import dataclass
import subprocess  # noqa: S404

@dataclass
class Binary:
	exec: str
	args: list[str]

	def run(self) -> subprocess.CompletedProcess:
		return subprocess.run([self.exec, *self.args], capture_output=True)