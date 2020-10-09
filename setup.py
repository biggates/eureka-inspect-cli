#!/usr/bin/env python

import ast
import re

from setuptools import Command, find_packages, setup
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('eureka_inspect_cli/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

description = 'CLI for quickly inspect nodes registered with eureka server'

install_requirements = [
    'click >= 7.1.2',
    'colorama >= 0.4.3',
    'requests >= 2.24.0',
]

setup(
    name='eureka_inspect_cli',
    author='biggates',
    author_email='biggates_2010@gmail.com',
    version=version,
    url='https://github.com/biggates/eureka-inspect-cli',
    packages=find_packages(),
    description=description,
    long_description=description,
    install_requires=install_requirements,
    entry_points={
        'console_scripts': ['eureka_inspect = eureka_inspect_cli.main:cli']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
