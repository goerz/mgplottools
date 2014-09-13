#!/usr/bin/env python

from distutils.core import setup
from mgplottools import __version__

setup(name='mgplottools',
      version=__version__,
      description='Collection of Utilities for plotting and visualization',
      author='Michael Goerz',
      author_email='mail@michaelgoerz.net',
      url='http://github.com/goerz/mgplottools',
      license='GPL',
      packages=['mgplottools']
     )
