from distutils.core import setup

from my_project import __version__
from setuptools import find_packages

setup(
    name="my_project",
    version=__version__,
    description="",
    author="Nick Jenkins",
    author_email="",
    url="",
    packages=find_packages(),
)
