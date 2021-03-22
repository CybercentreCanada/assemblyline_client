#!/bin/sh -x

python3.7 -m venv venv
venv/bin/pip install -U pip
venv/bin/pip install -U wheel
venv/bin/pip install -U pytest pytest-cov codecov flake8 pep8 autopep8 ipython cart assemblyline passlib mock pytest_mock
venv/bin/pip install -e .
