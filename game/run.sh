#!/bin/bash

cd "$(dirname "$0")" || exit 1

[ ! -d "venv" ] && python3 -m venv venv

source venv/bin/activate

[ -f "requirements.txt" ] && pip install -r requirements.txt

python3 -m app.main

deactivate
