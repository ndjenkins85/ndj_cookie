from distutils.core import setup

from setuptools import find_packages

from my_project import __version__

setup(
    name="my_project",
    version=__version__,
    description="",
    author="Nick Jenkins",
    author_email="",
    url="",
    packages=find_packages(),
)
