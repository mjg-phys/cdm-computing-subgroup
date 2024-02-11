#!/usr/bin/env python

import pathlib
from setuptools import setup

# Parent directory
HERE = pathlib.Path(__file__).parent

# The readme file
README = (HERE / "README.md").read_text()

setup(
    name="nuisance",
    version="1.0.2",
    description="Quick and dirty neutrino oscillations",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Stephan Meighen-Berger",
    author_email="stephan.meighenberger@unimelb.edu.au",
    url='https://github.com/MeighenBergerS/nu_isance',
    license="GNU",
    install_requires=[
        "PyYAML",
        "numpy",
        "scipy",
        "pandas",
        "tqdm",
        "numba"
    ],
    extras_require={
        "interactive": ["nbstripout", "matplotlib", "jupyter"],
    },
    packages=[
        "nu_isance",
        "nu_isance.utils",
        "nu_isance.errors",
        "nu_isance.nu_oscillations"
    ],
    package_data={'nu_isance': ["data/*.pkl"]},
    include_package_data=True
)