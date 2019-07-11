#!/bin/python3

from distutils.core import setup
# you may need setuptools instead of distutils

setup(
    name='ConvenienceFunctions',
    version='0.1',
    author='Tom Meyer',
    lilcense='GPLv3',
    url='https://github.com/Skasselbard/scripts',
    packages=['scripts'],
    scripts=['scripts/console.py'],
    install_requires=['serialpy']
)
