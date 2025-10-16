#!/bin/bash

[ ! -d "venv" ] && python3 -m venv venv
source venv/bin/activate
[ -f "requirements.txt" ] && pip install -r requirements.txt
python3 main.py
deactivate
