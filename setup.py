from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from python_wrapper import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, "README.rst"), encoding="utf-8") as file:
    readme = file.read()

with open(join(this_dir, "HISTORY.rst"), encoding="utf-8") as file:
    history = file.read()


class RunTests(Command):
    """Run all tests."""
    description = "run tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(
            [
                "py.test",
                "--cov=python_wrapper",
                "--cov-report=term-missing",
            ]
        )
        raise SystemExit(errno)


setup(
    name = "python-wrapper",
    version = __version__,
    description = "A generic Python API wrapper.",
    long_description = readme + "\n\n" + history,
    url = "https://github.com/cfc603/python-wrapper",
    author = "Trevor Watson",
    author_email = "wtrevor162@gmail.com",
    license = "MIT",
    classifiers = [
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords = "python-wrapper python_wrapper",
    packages = find_packages(exclude=["docs", "tests*"]),
    install_requires = ["requests", "simplejson"],
    extras_require = {
        "test": [
            "coverage",
            "flake8",
            "pytest",
            "pytest-cov",
            "responses",
            "tox",
        ],
    },
    use_2to3=True,
    cmdclass = {"test": RunTests},
)
