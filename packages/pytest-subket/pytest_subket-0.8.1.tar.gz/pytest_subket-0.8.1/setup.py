from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class build_py_with_pth_file(build_py):
    """Include the .pth file for this project, in the generated wheel."""

    pth_file = Path("src", "pytest_socket.pth")

    def run(self):
        super().run()

        target = Path(self.build_lib, self.pth_file.name)
        self.copy_file(self.pth_file, target, preserve_mode=0)


setup(cmdclass={"build_py": build_py_with_pth_file})
