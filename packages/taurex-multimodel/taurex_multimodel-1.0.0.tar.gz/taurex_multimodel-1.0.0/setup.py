#!/usr/bin/env python
import setuptools
from setuptools import find_packages
from setuptools import setup
#from numpy.distutils.core import Extension
#from numpy.distutils import log
import re, os

packages = find_packages(exclude=('tests', 'doc'))
provides = ['taurex_multimodel', ]

requires = []

version = "1.0.0" 

install_requires = ['taurex',]

entry_points = {'taurex.plugins': 'multimodel = taurex_multimodel'}#, 'console_scripts': console_scripts}

setup(name='taurex_multimodel',
      author="Quentin Changeat",
      author_email="",
      license="BSD",
      description='Plugin to compute models with multiple regions',
      packages=packages,
      version=version,
      url="https://github.com/groningen-exoatmospheres/taurex-multimodel",
      entry_points=entry_points,
      provides=provides,
      requires=requires,
      install_requires=install_requires)
