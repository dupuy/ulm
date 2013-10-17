#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Distribute/setuptools installation command."""

import os
import re

from setuptools import setup, find_packages


def read(file_name):
    """Return a (README) file as a string for use as long_description."""
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


def parse_requirements(file_name):
    """Parses a pip requirements file and returns a list of packages.

    Use the result of this function in the ``install_requires`` field.
    Copied from cburgmer/pdfserver.

    """
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # should also support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):
    """Parses a pip requirements file and returns a list of dependencies.

    Use the result of this function in the ``dependency_links`` field.
    Copied from cburgmer/pdfserver.

    """
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links

setup(
    name="ulm",
    version="0.1",
    author="Alexander Dupuy",
    author_email="alex.dupuy@mac.com",
    description=("Ubuntu Laptop Monitoring - "
                 "Django project for Wifi and battery status"),
    long_description=read('README.rst'),
    license="BSD",
    keywords="django laptop monitoring dbus battery wifi",
    url="http://github.com/dupuy/ulm/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements('requirements/base.txt'),
    dependency_links=parse_dependency_links('requirements/base.txt'),
    entry_points={
        'console_scripts': [
            'ulm = ulm.runner:main',
            ],
        },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: Linux",
        "Programming Language :: Python",
    ],
)
