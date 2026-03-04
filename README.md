# 📦 Sistema de Gestión de Inventario

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-6.0-darkgreen?style=for-the-badge&logo=django)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-UI-38B2AC?style=for-the-badge&logo=tailwindcss)
![Chart.js](https://img.shields.io/badge/Charts-Chart.js-FF6384?style=for-the-badge&logo=chartdotjs)
![Render](https://img.shields.io/badge/Deploy-Render-000000?style=for-the-badge&logo=render)
![Gunicorn](https://img.shields.io/badge/Server-Gunicorn-499848?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Aplicación web desarrollada con **Django + Tailwind CSS** para la gestión inteligente de inventario.

Este proyecto forma parte de mi evolución como desarrollador Full Stack y ha sido construido con un enfoque realista: arquitectura limpia, permisos, métricas y despliegue en producción.

---

## 🚀 Demo

🔗 https://sistema-inventario-9vkg.onrender.com

---

## 🧠 Objetivo del Proyecto

Construir un MVP funcional que permita:

- Gestión completa de productos
- Control de stock mediante movimientos
- Métricas visuales en dashboard
- Importación y exportación de datos
- Sistema de autenticación y permisos
- Despliegue en producción

---

## 🛠️ Stack Tecnológico

- **Backend:** Django  
- **Frontend:** Django Templates + Tailwind CSS  
- **Base de datos:** SQLite (MVP)  
- **Gráficos:** Chart.js  
- **Autenticación:** Django Auth + sistema de roles  
- **Despliegue:** Render  
- **Servidor WSGI:** Gunicorn  
- **Archivos estáticos:** WhiteNoise  

---

## 📊 Funcionalidades

### 📦 Productos
- CRUD completo
- Filtros avanzados
- Paginación reutilizable
- Indicador de stock bajo
- Importación desde CSV
- Exportación con filtros aplicados

### 🔄 Movimientos de Stock
- Entradas y salidas
- Control automático del stock
- Validación para evitar stock negativo
- Filtros por fecha, tipo y producto
- Exportación CSV

### 📈 Dashboard
- Valor total del inventario
- Productos con stock bajo
- Productos por categoría
- Entradas vs salidas (gráfico)
- Métricas clave del sistema

### 🔐 Autenticación y Permisos
- Registro y login
- Sistema de grupos:
  - Administrador
  - Usuario estándar
- Protección de vistas
- Página 403 personalizada

---

## 🏗️ Arquitectura

El stock no se edita manualmente.

Se calcula exclusivamente a través de movimientos:

- Entrada → suma stock
- Salida → resta stock
- Validación para evitar valores negativos

Esto asegura consistencia de datos y trazabilidad.

---

## 📂 Instalación Local

```bash
git clone https://github.com/tuusuario/inventory.git
cd inventory

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## 🧾 Producción

Configuración importante en `settings.py`:

```python
DEBUG = False
STATIC_ROOT = BASE_DIR / "staticfiles"
```

Luego ejecutar:

```bash
python manage.py collectstatic
```

En Render, el comando de arranque:

```bash
gunicorn inventory.wsgi
```

---

## 🎯 Estado del Proyecto

Actualmente el proyecto funciona como MVP completamente operativo.

Próximos pasos potenciales:

- Multiusuario por empresa
- Sistema SaaS con suscripción
- Migración a PostgreSQL
- API REST
- Panel de administración más avanzado

---

## 📌 Aprendizajes Clave

- Gestión real de estado en aplicaciones CRUD
- Control de permisos y roles en Django
- Optimización de consultas con `select_related`
- Paginación reutilizable
- Manejo correcto de archivos estáticos en producción
- Deploy completo en Render
- Arquitectura preparada para escalar

---

## 👨‍💻 Autor

Desarrollado como parte de mi formación en el Máster Full Stack.

Actualmente evolucionando hacia proyectos más complejos y orientados a producto real.