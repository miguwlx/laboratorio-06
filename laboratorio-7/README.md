# Laboratorio 7 — ClassroomHub: persistencia con MySQL o MariaDB

Continúa el Laboratorio 6: el catálogo deja de ser una lista fija y pasa a guardarse en **MySQL o MariaDB** mediante modelos (`Category`, `Resource`), migraciones, ORM y Django Admin.

## Versiones

- Python 3.12 o superior
- Django 6.1.3
- `mysqlclient` y `python-dotenv` (ver `requirements.txt`)

## Base de datos (MariaDB o MySQL)

Requiere un servidor **MariaDB ≥ 10.11** o **MySQL ≥ 8.4** (con Django 5.2 LTS: MariaDB ≥ 10.5 / MySQL ≥ 8.0.11).
Para compilar `mysqlclient` en Linux hacen falta `libmariadb-dev`, `pkg-config` y un compilador; en Windows normalmente `pip` instala una versión ya compilada.

Con una cuenta administrativa (cambia la contraseña; usa solo letras y números para evitar problemas al pegar):

```sql
CREATE DATABASE IF NOT EXISTS classroom_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'classroomhub_user'@'127.0.0.1' IDENTIFIED BY 'tu_contrasena_privada';
CREATE USER IF NOT EXISTS 'classroomhub_user'@'localhost' IDENTIFIED BY 'tu_contrasena_privada';
GRANT ALL PRIVILEGES ON classroom_hub.* TO 'classroomhub_user'@'127.0.0.1';
GRANT ALL PRIVILEGES ON classroom_hub.* TO 'classroomhub_user'@'localhost';
GRANT ALL PRIVILEGES ON test_classroom_hub.* TO 'classroomhub_user'@'127.0.0.1';
GRANT ALL PRIVILEGES ON test_classroom_hub.* TO 'classroomhub_user'@'localhost';
```

> En Windows el servidor puede ver la conexión como `localhost` aunque uses `127.0.0.1`; por eso se crea la cuenta para ambos hosts.
> Ejecuta cada instrucción terminada en `;` **dentro** del cliente SQL, no en CMD.

Copia `.env.example` como `.env` y escribe en `DB_PASSWORD` la misma contraseña (sin comillas ni espacios):

```bash
copy .env.example .env      # Windows
cp .env.example .env        # Linux / macOS
```

`.env` **no se versiona**; `.env.example` solo contiene valores demostrativos.

## Instalación

```bash
python -m venv .venv
# Windows (CMD):        .venv\Scripts\activate
# Linux / macOS:        source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Crear tablas y administrador

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Entra en http://127.0.0.1:8000/admin/ y crea al menos una categoría y un recurso. Aparecerán en `/resources/` y permanecerán al reiniciar el servidor.

Migraciones incluidas: `0001_initial` (tablas) y `0002_resource_resource_type` (campo opcional `resource_type`).

## Rutas

- `/` — página principal
- `/resources/` — catálogo leído de la base mediante el ORM
- `/about/` — propósito del proyecto
- `/admin/` — administración de categorías y recursos

## Pruebas

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test pages
```

Resultado esperado: **10 pruebas** en `OK`, ejecutadas sobre la base descartable `test_classroom_hub` (nunca sobre `classroom_hub`).

## Todavía no incluye

- Registro, login y permisos (Laboratorio 8)
- Formularios públicos y CRUD (Laboratorio 9)
- API REST
