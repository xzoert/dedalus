#!/usr/bin/env python3


from distutils.core import setup

setup(
    # Application name:
    name="dedalus",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="xzoert",
    author_email="xzoert@gmail.com",

    # Packages
    packages=["dedalus","dedalus.test","dedalus.ui","dedalus.ui.test","dedalus.ui.icons","dedalus.ui.tagger"],

    # Details
    url="",

    #
    license="LICENSE.txt",
    
    description="Dedalus.",

    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    requires=[
        "PySide",
    ],
)

