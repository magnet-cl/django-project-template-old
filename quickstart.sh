#!/bin/bash

./install/install-prerequisites
virtualenv .env --distribute
.env/bin/pip install --requirement install/requirements.pip
source .env/bin/activate
cp core/local_settings.py.default core/local_settings.py
