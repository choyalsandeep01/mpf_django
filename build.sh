#!/usr/bin/env bash

# --- ALWAYS upgrade build tools first ---
python -m pip install --upgrade pip setuptools wheel

# --- NOW install your app's dependencies ---
pip install -r requirements.txt

# --- Django housekeeping ---
python manage.py collectstatic --no-input
python manage.py migrate
