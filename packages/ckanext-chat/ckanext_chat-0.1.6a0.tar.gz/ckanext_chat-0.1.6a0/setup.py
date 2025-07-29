# -*- coding: utf-8 -*-
from codecs import open  # To use a consistent encoding
from os import environ, path

from setuptools import (  # Always prefer setuptools over distutils
    find_packages, setup)

here = path.abspath(path.dirname(__file__))


# Get the long description from the relevant file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read().splitlines()

setup(
    name="""ckanext-chat""",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=environ.get("VERSION", "0.0.0"),
    description="""Extension adds a pydantic ai chat interface to CKAN, that can run actions with user aware context.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    # The project's main homepage.
    url="https://github.com/Mat-O-Lab/ckanext-chat",
    # Author details
    author="""Thomas Hanke""",
    author_email="""thomas.hanke@iwm.fraunhofer.de""",
    # Choose your license
    license="AGPL",
    message_extractors={
        "ckanext": [
            ("**.py", "python", None),
            ("**.js", "javascript", None),
            ("**/templates/**.html", "ckan", None),
        ],
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points="""
        [ckan.plugins]
        chat=ckanext.chat.plugin:ChatPlugin
    """,
)
