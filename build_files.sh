#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
# ou toute autre commande de build nécessaire
