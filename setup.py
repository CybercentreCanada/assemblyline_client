#!/usr/bin/env python
"""Assemblyline Client Library PiP Installer"""

import os
from setuptools import setup, find_packages

# For development and local builds use this version number, but for real builds replace it
# with the tag found in the environment
package_version = "4.0.0.dev0"
if 'BITBUCKET_TAG' in os.environ:
    package_version = os.environ['BITBUCKET_TAG'].lstrip('v')
elif 'BUILD_SOURCEBRANCH' in os.environ:
    full_tag_prefix = 'refs/tags/v'
    package_version = os.environ['BUILD_SOURCEBRANCH'][len(full_tag_prefix):]

# read the contents of the README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='assemblyline-client',
    version=package_version,
    description='Assemblyline v4 client library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/CybercentreCanada/assemblyline_client',
    author='CSE-CST Assemblyline development team',
    author_email='assemblyline@cyber.gc.ca',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    entry_points={
        'console_scripts': [
            'al-submit=assemblyline_client.submit:main',
        ],
    },
    install_requires=[
        'pycryptodome',
        'requests',
        'requests[security]',
        'python-baseconv',
        'python-socketio[client]',
        'socketio-client==0.5.7.4'
    ],
    extras_require={
        'test': [
            'pytest',
            'cart',
            'assemblyline',
        ]
    },
    keywords='development assemblyline client gc canada cse-cst cse cst',
    packages=find_packages(exclude=['test/*'])
)
