#!/usr/bin/env bash
# build.sh

# Instala dependências e prepara o Django
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
