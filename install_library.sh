#!/usr/bin/env bash

#Constants are defined here
SOURCE_DIR=./virtualenv/bin/activate


# Install script
source ${SOURCE_DIR} && \
    python setup.py bdist_wheel && \
    pip install -r requirements.txt --upgrade dist/imclas-*