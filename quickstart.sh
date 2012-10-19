#!/bin/bash

./install/install-prerequisites
virtualenv .env --distribute
source .env/bin/activate
easy_install -U distribute
.env/bin/pip install --requirement install/requirements.pip
cp config/local_settings.py.default config/local_settings.py
