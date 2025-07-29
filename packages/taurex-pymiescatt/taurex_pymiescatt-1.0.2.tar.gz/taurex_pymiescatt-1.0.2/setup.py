import setuptools
from setuptools import find_packages
from setuptools import setup
#from numpy.distutils.core import Extension
#from numpy.distutils import log
import re, os

packages = find_packages(exclude=('tests', 'doc'))
provides = ['taurex_pymiescatt', ]

requires = ['PyMieScatt']

install_requires = ['taurex']

version = "1.0.2" 

entry_points = {'taurex.plugins': 'taurex_pymiescatt = taurex_pymiescatt'}

setup(name='taurex_pymiescatt',
      author="Quentin Changeat",
      author_email="q.changeat@rug.nl",
      license="BSD",
      description='Cloud retrieval capabilities for TauREx',
      packages=packages,
      version=version,
      url="https://github.com/groningen-exoatmospheres/taurex-pymiescatt",
      entry_points=entry_points,
      provides=provides,
      requires=requires,
      install_requires=install_requires)
