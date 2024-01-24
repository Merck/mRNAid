#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
from io import open

about = {}
# Read version number from __version__.py (see PEP 396)
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'mrnaid', '__version__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

# Read contents of readme file into string
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read dependencies from requirements.txt
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = [l.strip() for l in f.readlines() if l.strip()]

setup(
    name='mRNAid',
    version=about['__version__'],
    description='mRNAid: experimentally validated open-source tool for optimization and visualisation of mRNA molecules',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nikita Vostrosablin',
    packages=find_packages(include=['mrnaid.backend.*', 'mrnaid.cli.*', 'mrnaid', 'mrnaid.backend', 'mrnaid.cli']),
    license='MIT',
    python_requires=">=3.8",
    install_requires=install_requires,
    keywords='mrna, mrnaid, optimization',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,
    package_data={'': ['*.js', '*.css', '*.html', '*.png', '*.svg', '*.json']},
    url='https://github.com/Merck/mRNAid',
    entry_points={
        'console_scripts': ['mrnaid = mrnaid.cli.main:main']
    }
)
