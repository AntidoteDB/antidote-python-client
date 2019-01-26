#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 21:36:45 2019

@author: nmp
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="antidotedb",
    version="0.1",
    author="Nuno Preguica",
    author_email="nuno.preguica@fct.unl.pt",
    description="AntidoteDB Python clients",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AntidoteDB/antidote-python-client/tree/master/src/main/python/antidotedb",
    packages=['antidotedb','antidotedb.proto'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'protobuf',
      ],
)
