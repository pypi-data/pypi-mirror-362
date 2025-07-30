#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'python-magic>=0.4.15', 'dateutils>=0.6.6',
    'xmltodict>=0.12.0', 'pyyaml>=5.1.2', 'chibi-donkey>=1.0.1',
    'chibi-atlas>=1.0.2' ]

setup(
    name='chibi',
    keywords='chibi',
    version='0.17.0',
    description='python snippets and other useful things',
    long_description=readme + '\n\n' + history,
    license="WTFPL",
    author='dem4ply',
    author_email='dem4ply@gmail.com',
    packages=find_packages(include=['chibi', 'chibi.*']),
    install_requires=requirements,
    dependency_links = [],
    url='https://github.com/dem4ply/chibi',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Utilities',
    ] )
