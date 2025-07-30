from setuptools import setup, find_packages, Command
import os
from shutil import rmtree
import sys

here = os.path.abspath(os.path.dirname(__file__))
VERSION="0.1.3"

class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
            rmtree(os.path.join(here, "build"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        # self.status('Pushing git tags…')
        # os.system('git tag v{0}'.format(about['__version__']))
        # os.system('git push --tags')

        sys.exit()

EXTRAS = {
    'syntax': ['textual[syntax]'],
}

setup(
    name="ted-editor",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        "textual>=0.1.18",
    ],
    entry_points={
        "console_scripts": [
            "ted = ted.cli:main",
        ],
    },
    extras_require=EXTRAS,
    author="James Brown",
    author_email="randomvoidmail@foxmail.com",
    description="Terminal Text Editor with TUI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/James4Ever0/ted",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    package_data={
        "ted": ["*.css"],
    },
    cmdclass={
        "upload": UploadCommand,
    },
)
