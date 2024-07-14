#!/usr/bin/env python

import pathlib
from setuptools import setup

# Parent directory
HERE = pathlib.Path(__file__).parent

# The readme file
README = (HERE / "README.md").read_text()

setup(
    name="DetectorExample",
    version="0.0.1",
    description="A basic simulation chain",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Stephan Meighen-Berger",
    author_email="stephan.meighenberger@gmail.com",
    url='https://github.com/MeighenBergerS/cdm_detector_example',
    license="GNU",
    install_requires=[
        "PyYAML",
        "numpy",
        "scipy"
    ],
    extras_require={
        "interactive": ["nbstripout", "matplotlib", "jupyter", "tqdm"],
    },
    packages=["detectorexample"],
    package_data={'detectorexample': ["data/*.pkl"]},
    include_package_data=True
)
