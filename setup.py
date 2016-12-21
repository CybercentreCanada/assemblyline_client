"""Assemblyline Client Library PiP Installer"""

from setuptools import setup

import assemblyline_client

setup(
    name='assemblyline_client',
    version='.'.join(map(str, assemblyline_client.__build__)),
    description='Assemblyline Client Library',
    long_description="The Assemblyline Client Library facilitates issuing requests to assemblyline.",
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'al-submit=assemblyline_client.submit:main',
        ],
    },
    install_requires=['requests', 'socketio-client==0.5.6', 'requests[security]'],
    keywords='assemblyline',
    packages=['assemblyline_client'],
)
