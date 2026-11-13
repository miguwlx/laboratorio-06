# Laboratorio 9 — ClassroomHub: formularios y CRUD

Continúa el Laboratorio 8: CRUD de recursos con `ModelForm`, vistas genéricas (`DetailView`, `CreateView`, `UpdateView`, `DeleteView`) y un permiso distinto para cada operación.

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

No hay modelos nuevos ni migraciones nuevas en este laboratorio.

## Grupos (Catalog reviewers y Catalog editors)

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

Grupo **Catalog editors** (ver, añadir, cambiar y eliminar recursos):

```python
required_codes = ["view_resource", "add_resource", "change_resource", "delete_resource"]
permissions = list(Permission.objects.filter(content_type=content_type, codename__in=required_codes))
editors, _ = Group.objects.get_or_create(name="Catalog editors")
editors.permissions.add(*permissions)
```

Los permisos **no** se asignan mediante el formulario de registro público: un administrador asigna `Catalog editors` a una cuenta de prueba desde Django Admin. Las categorías se siguen gestionando desde `/admin/` (crea algunas antes de crear recursos).

## Rutas

```text
GET  /resources/                   público
GET  /resources/<pk>/              público (404 si no existe)
GET  /resources/new/               add_resource
POST /resources/new/
GET  /resources/<pk>/edit/         change_resource
POST /resources/<pk>/edit/
GET  /resources/<pk>/delete/       delete_resource (solo confirmación, no borra)
POST /resources/<pk>/delete/       delete_resource (borra)
GET  /resources/review/            view_resource
/accounts/signup/  /accounts/login/  /accounts/logout/ (POST)  /dashboard/  /admin/
```

Sin sesión se redirige al login; con sesión pero sin permiso se responde `403`.

## Pruebas

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test pages
```

Resultado: **58 pruebas** en `OK` (28 de los laboratorios 7 y 8 + 30 del CRUD), sobre `test_classroom_hub`.

> Nota: el texto del laboratorio menciona 27 pruebas nuevas y 55 en total, pero la clase `ResourceCrudTests` que proporciona contiene 30 métodos de prueba, por lo que el total real es 58.

## Todavía no incluye

- CRUD público de categorías (se gestionan en Django Admin)
- Carga de archivos, API REST, paginación y filtros avanzados
- Despliegue a producción: un CRUD expuesto en Internet requiere revisar seguridad, errores y validaciones de negocio
