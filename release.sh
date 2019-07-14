#!/bin/bash

if [[ "$1" == "build" ]]; then
    python3 setup.py sdist bdist_wheel
    exit
fi

if [[ "$1" == "upload-test" ]]; then
    python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    exit
fi

if [[ "$1" == "upload" ]]; then
   python -m twine upload --repository-url https://pypi.org/legacy/ dist/*
fi


