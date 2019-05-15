import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyutl",
    version="2.1",
    author="Josue Gomez",
    author_email="jgomez@binkfe.com",
    description="A package of utilities for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.binkfe.com/jesrat/pyutils",
    packages=['pyutl'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
