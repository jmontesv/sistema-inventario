#!/usr/bin/env bash

# Instala dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate --noinput

# Archivos estáticos
python manage.py collectstatic --noinput
