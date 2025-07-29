#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup

sys.path.insert(0, os.path.dirname(__file__))

try:
    from version import __version__
except ImportError:
    __version__ = '0.0.1'

__author__ = 'Akinon'
__license__ = 'MIT'
__maintainer__ = 'Akinon'
__email__ = 'dev@akinon.com'

if sys.version_info[0] == 2:
    from io import open

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='dj-whisperer',
    version=__version__,
    author=__author__,
    author_email=__email__,
    maintainer=__maintainer__,
    maintainer_email=__email__,
    description='Stay informed of it',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=__license__,
    url='https://bitbucket.org/akinonteam/dj-whisperer',
    project_urls={
        'Documentation': 'https://dj-whisperer.readthedocs.io',
        'Source Code': 'https://bitbucket.org/akinonteam/dj-whisperer',
    },
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    platforms='any',
    zip_safe=False,
    use_scm_version={
        'write_to': './version.py',
        'write_to_template': '__version__ = "{version}"\n',
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
    ],
)
