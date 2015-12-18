#! /usr/bin/python
"""Setuptools-based setup script for becksteinlab-kernels.

For a basic installation just type the command::

  python setup.py install

"""

from setuptools import setup

setup(name='beckernels',
      version='0.1.0-dev',
      author='David Dotson',
      author_email='dotsdl@gmail.com',
      packages=['beckernels',
                'beckernels.dmdmd'],
      scripts=[],
      license='MIT',
      long_description=open('README.md').read(),
      install_requires=['radical.ensemblemd']
      )
