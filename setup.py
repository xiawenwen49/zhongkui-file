import codecs
import os
import re
import sys
from distutils.util import strtobool

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """
    Provide a Test runner to be used from setup.py to run unit tests
    """

    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


def open_local(paths, mode="r", encoding="utf8"):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *paths)

    return codecs.open(path, mode, encoding)


with open_local(["src/python/zhongkui/file", "__init__.py"],
                encoding="latin1") as fp:
    try:
        version = re.findall(r"^__version__ = \"([^']+)\"\r?$", fp.read(),
                             re.M)[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

setup(
    name="zhongkui-file",
    version=version,
    url="https://git.kongkongss.com/jyker/zhongkui-file",
    author="Kongkong Jiang",
    author_email="jyk.kongkong@gmail.com",
    description="Zhongkui file utils package",
    keywords="Zhongkui file",
    license="MIT",
    python_requires=">=3.7.3",
    packages=find_packages('src/python'),
    package_dir={'': 'src/python'},
    include_package_data=True,
    namespace_packages=['zhongkui'],
    cmdclass={"test": PyTest},
    install_requires=[
        "file-magic >= 0.4.0", "pefile >= 2019.4.18", "pytest >= 5.0.1"
    ])