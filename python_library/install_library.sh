#!/usr/bin/env bash

#Constants are defined here
SOURCE_DIR=./virtualenv/bin/


# Install script
${SOURCE_DIR}/python setup.py bdist_wheel && \
    ${SOURCE_DIR}/pip install -r requirements.txt -U dist/imclas-*