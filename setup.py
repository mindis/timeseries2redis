#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERSION = '0.1'
#
import sys
import os
from setuptools import setup, find_packages
from setuptools.extension import Extension


setup(name='timeseries2redis',
      version=VERSION,
      description='timeseries2redis',
      author='trbck',
      packages=find_packages(),
      package_data={'timeseries2redis': ['timeseries2redis.py']},
      )
