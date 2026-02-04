#!/usr/bin/env bash

# Instalar dependencias Python
pip install -r requirements.txt

# Compilar Tailwind (asegúrate de que npm/yarn esté disponible en el entorno)
npx tailwindcss -i ./static/src/input.css -o ./static/dist/styles.css --minify

# Migraciones
python manage.py migrate --noinput

# Copiar estáticos a STATIC_ROOT
python manage.py collectstatic --noinput
