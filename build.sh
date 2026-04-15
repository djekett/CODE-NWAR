#!/usr/bin/env bash
# Script de build pour Render.com (ou tout PaaS compatible).
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input
