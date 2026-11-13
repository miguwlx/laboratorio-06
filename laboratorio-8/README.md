# Laboratorio 8 — ClassroomHub: autenticación, sesiones y permisos

Continúa el Laboratorio 7: registro de cuentas con `UserCreationForm`, login y logout con las vistas integradas de Django, panel privado con sesión y una vista de revisión protegida por el permiso `pages.view_resource`.

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

## Grupo revisor (Catalog reviewers)

Después de `migrate`, crea el grupo desde Django Admin o desde el shell (`python manage.py shell`):

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from pages.models import Resource

content_type = ContentType.objects.get_for_model(Resource)
view_permission = Permission.objects.get(content_type=content_type, codename="view_resource")
reviewers, _ = Group.objects.get_or_create(name="Catalog reviewers")
reviewers.permissions.add(view_permission)
```

Asigna el grupo a una cuenta desde Django Admin. El registro público **nunca** concede privilegios.

## Rutas

- `/` , `/resources/` , `/about/` — públicas
- `/accounts/signup/` — registro (cuentas sin privilegios)
- `/accounts/login/` — inicio de sesión
- `/accounts/logout/` — cierre de sesión (solo `POST`; `GET` devuelve 405)
- `/dashboard/` — panel privado con contador de sesión
- `/resources/review/` — revisión del catálogo: anónimo → login, cuenta sin permiso → 403, `Catalog reviewers` → 200
- `/admin/` — administración

## Pruebas

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test pages
```

Resultado esperado: **28 pruebas** en `OK` (10 del Laboratorio 7 + 18 nuevas), sobre `test_classroom_hub`.

Estar autenticado no equivale a estar autorizado: las pruebas cubren los flujos implementados, no son una auditoría de seguridad.

## Todavía no incluye

- Formularios y CRUD públicos (Laboratorio 9)
- OAuth, autenticación multifactor, recuperación de contraseña por correo
- Despliegue a producción
