#!/usr/bin/env bash

# Instalar dependencias Python
pip install -r requirements.txt

# Migraciones
python manage.py migrate --noinput

# Copiar estáticos a STATIC_ROOT
python manage.py collectstatic --noinput
