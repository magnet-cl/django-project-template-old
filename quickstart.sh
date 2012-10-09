#!/bin/bash

./install/install-prerequisites
virtualenv .env --distribute
source .env/bin/activate
easy_install -U distribute
.env/bin/pip install --requirement install/requirements.pip
cp core/local_settings.py.default core/local_settings.py
