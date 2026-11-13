# Laboratorio 6 — ClassroomHub: fundamentos de Django

Portal de recursos de aprendizaje construido con Django: tres páginas navegables, una plantilla base compartida y datos de ejemplo definidos en las vistas. Primera parte de la secuencia (URL → vista → plantilla → respuesta).

## Versiones

- Python 3.12 o superior
- Django 6.1.3

## Instalación

```bash
python -m venv .venv
# Windows (CMD):        .venv\Scripts\activate
# Linux / macOS:        source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecutar

```bash
python manage.py check
python manage.py runserver
```

Abre http://127.0.0.1:8000/

## Rutas

- `/` — página principal
- `/resources/` — lista de recursos (datos de ejemplo)
- `/about/` — propósito del proyecto
- Cualquier otra ruta devuelve `404`

## Pruebas

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test pages
```

Resultado esperado: **5 pruebas** en `OK` (`SimpleTestCase`, sin base de datos).

## Todavía no incluye

- Base de datos propia, modelos y migraciones (Laboratorio 7)
- Inicio de sesión y permisos (Laboratorio 8)
- Formularios y CRUD (Laboratorio 9)
- Los recursos son datos de ejemplo: los cambios no se guardan
