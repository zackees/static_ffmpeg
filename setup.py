import os
import sys
from shutil import rmtree
from setuptools import setup, Command

class UploadCommand(Command):
    """Support setup.py upload."""
    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        pass

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(os.path.dirname(__file__), "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system('"{0}" setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v2.8")
        os.system("git push --tags")

        sys.exit()

if __name__ == '__main__':
    setup(
        cmdclass={
            "upload": UploadCommand,
        },
    )
