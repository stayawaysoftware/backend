#!/bin/bash

python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r ./configs/requirements-dev.txt
python3 -m pip install -r ./configs/requirements-test.txt
python3 -m pip install -r ./configs/requirements-utils.txt
