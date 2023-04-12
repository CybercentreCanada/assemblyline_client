#!/bin/sh -x

python3 -m venv venv
venv/bin/pip install -U pip
venv/bin/pip install -U wheel
venv/bin/pip install -U pytest flake8 pep8 autopep8 ipython cart assemblyline passlib
venv/bin/pip install -e .
