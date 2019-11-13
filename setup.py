import pyutl as pkg
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=pkg.__title__,
    version=pkg.__version__,
    author=pkg.__author__,
    author_email=pkg.__email__,
    description=pkg.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=pkg.__url__,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
