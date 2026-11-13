# ClassroomHub — laboratorios de Django

Este repositorio reúne los laboratorios 6 a 9 de ClassroomHub, un catálogo de recursos de aprendizaje desarrollado progresivamente con Django. Cada laboratorio es una aplicación independiente: usa su propio código, entorno virtual y configuración; ejecuta los comandos desde la carpeta del laboratorio que quieras probar.

## Tecnologías y requisitos

- Python 3.12 o superior.
- Django 6.1.3.
- Laboratorios 7, 8 y 9: MySQL 8.4 o superior, o MariaDB 10.11 o superior; `mysqlclient` y `python-dotenv` (dependencias declaradas en cada `requirements.txt`).
- Laboratorio 6: SQLite según su configuración; no requiere configurar un servidor MySQL/MariaDB.

En Windows, instala Python y asegúrate de que `python` esté disponible en PowerShell. Para los laboratorios 7 a 9 instala y ejecuta localmente un servidor MySQL o MariaDB compatible con las versiones indicadas en sus README. En Linux, compilar `mysqlclient` puede requerir bibliotecas de desarrollo de MariaDB, `pkg-config` y un compilador.

## Estructura

```text
laboratorio-6/   Fundamentos de Django y plantillas
laboratorio-7/   Modelos y persistencia con MySQL/MariaDB
laboratorio-8/   Autenticación, sesiones y permisos
laboratorio-9/   Formularios, CRUD y permisos
classroom-hub/   Proyecto Django independiente que ya existía
config/, pages/, manage.py, requirements.txt
                 Proyecto Django histórico ubicado en la raíz
```

`classroom-hub/` y el proyecto de la raíz contienen archivos propios y se conservan; esta guía se centra en los cuatro laboratorios. Los README de cada laboratorio siguen siendo la referencia para sus detalles específicos.

## Qué incluye cada laboratorio

- **Laboratorio 6:** rutas, vistas y plantillas de Django; presenta páginas y recursos de ejemplo, sin persistencia propia del catálogo.
- **Laboratorio 7:** modelos `Category` y `Resource`, migraciones, ORM, Django Admin y persistencia en MySQL o MariaDB.
- **Laboratorio 8:** registro, inicio y cierre de sesión, panel privado y acceso de revisión mediante permisos y el grupo `Catalog reviewers`.
- **Laboratorio 9:** detalle y CRUD de recursos con `ModelForm` y vistas genéricas; las operaciones requieren sus permisos correspondientes. Las categorías se administran desde Django Admin.

## Preparar y ejecutar un laboratorio

Los siguientes comandos se ejecutan **desde la carpeta del laboratorio**. Repite la preparación para cada uno; no compartas un entorno virtual entre laboratorios.

### Windows (PowerShell)

Ejemplo para el Laboratorio 6:

```powershell
cd laboratorio-6
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Para los demás, cambia `cd laboratorio-6` por `cd laboratorio-7`, `cd laboratorio-8` o `cd laboratorio-9`. Si PowerShell bloquea la activación del entorno, puedes usar una terminal CMD y ejecutar `.\.venv\Scripts\activate.bat`, o invocar el intérprete del entorno directamente.

### Linux y macOS

Desde la carpeta del laboratorio elegido:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

El servidor de desarrollo queda normalmente en <http://127.0.0.1:8000/>. Deténlo con `Ctrl+C`. Si el puerto está ocupado, puedes indicar otro, por ejemplo `python manage.py runserver 8001`.

## Base de datos para los laboratorios 7, 8 y 9

Estos tres laboratorios configuran el motor MySQL y leen `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT` del archivo `.env`. El ejemplo usa la base `classroom_hub`, el usuario `classroomhub_user`, el host `127.0.0.1` y el puerto `3306`. El valor de contraseña del ejemplo es solo un marcador: reemplázalo localmente por una contraseña propia y no la publiques.

1. Inicia el servidor MySQL o MariaDB.
2. Desde el cliente SQL y con una cuenta administrativa, crea la base y un usuario local. Sustituye `REEMPLAZAR_LOCALMENTE` por la contraseña elegida:

   ```sql
   CREATE DATABASE IF NOT EXISTS classroom_hub
     CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER IF NOT EXISTS 'classroomhub_user'@'127.0.0.1'
     IDENTIFIED BY 'REEMPLAZAR_LOCALMENTE';
   CREATE USER IF NOT EXISTS 'classroomhub_user'@'localhost'
     IDENTIFIED BY 'REEMPLAZAR_LOCALMENTE';
   GRANT ALL PRIVILEGES ON classroom_hub.* TO 'classroomhub_user'@'127.0.0.1';
   GRANT ALL PRIVILEGES ON classroom_hub.* TO 'classroomhub_user'@'localhost';
   GRANT ALL PRIVILEGES ON test_classroom_hub.* TO 'classroomhub_user'@'127.0.0.1';
   GRANT ALL PRIVILEGES ON test_classroom_hub.* TO 'classroomhub_user'@'localhost';
   ```

3. En la carpeta del laboratorio, copia `.env.example` a `.env` y pon la misma contraseña local en `DB_PASSWORD`. Si `.env` ya existe, consérvalo y actualiza solo los valores que necesites; no lo sobrescribas.

   PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

   CMD:

   ```bat
   copy .env.example .env
   ```

   Linux/macOS:

   ```bash
   cp .env.example .env
   ```

   `.env` está excluido por Git; conserva y comparte únicamente `.env.example`, sin credenciales privadas.

4. Con el entorno virtual activado y desde esa misma carpeta, crea las tablas y, si vas a usar Django Admin, una cuenta administrativa:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

El laboratorio 6 no necesita esta configuración MySQL/MariaDB. Cada laboratorio de la serie usa la misma configuración de base de datos, pero ejecuta sus propias migraciones desde su propio directorio.

## Rutas principales

Usa el mismo host local del servidor; las rutas siguientes se añaden a `http://127.0.0.1:8000`.

| Laboratorio | Rutas |
|---|---|
| 6 | `/`, `/resources/`, `/about/` |
| 7 | `/`, `/resources/`, `/about/`, `/admin/` |
| 8 | `/`, `/resources/`, `/about/`, `/accounts/signup/`, `/accounts/login/`, `/accounts/logout/`, `/dashboard/`, `/resources/review/`, `/admin/` |
| 9 | Rutas del laboratorio 8 y CRUD: `/resources/<pk>/`, `/resources/new/`, `/resources/<pk>/edit/`, `/resources/<pk>/delete/` |

El cierre de sesión del laboratorio 8 y las operaciones de creación, edición y eliminación del laboratorio 9 usan solicitudes POST. Para las rutas privadas, estar autenticado no sustituye al permiso requerido. En los laboratorios 8 y 9 configura los grupos y permisos descritos en sus README individuales.

## Pruebas y comprobaciones

Desde la carpeta de cada laboratorio, sus README documentan estos comandos:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test pages
```

Los laboratorios 7 a 9 necesitan una conexión MySQL/MariaDB válida y permisos sobre la base de pruebas `test_classroom_hub` para ejecutar su suite. Estos comandos describen las pruebas disponibles; no implican que se hayan ejecutado en cada entorno.

## Solución de problemas comunes

- **Faltan `DB_NAME`, `DB_USER` o `DB_PASSWORD`:** comprueba que copiaste `.env.example` como `.env` en la carpeta del laboratorio 7, 8 o 9 y que completaste sus valores locales.
- **No se puede conectar a MySQL/MariaDB:** verifica que el servicio esté iniciado, que `DB_HOST` y `DB_PORT` sean correctos y que el usuario tenga permisos sobre `classroom_hub` y `test_classroom_hub`.
- **Falla la instalación de `mysqlclient`:** en Linux puede ser necesario instalar las bibliotecas de desarrollo de MariaDB/MySQL, `pkg-config` y un compilador; consulta el README del laboratorio y los requisitos de tu sistema.
- **No existe una tabla o el admin falla:** activa el entorno correcto y ejecuta `python manage.py migrate` desde la carpeta del laboratorio correspondiente.
- **Una ruta privada responde con redirección al login o con 403:** inicia sesión y confirma que la cuenta tenga el grupo y permiso indicados en el README del laboratorio.
- **El puerto 8000 está ocupado:** inicia Django con otro puerto, por ejemplo `python manage.py runserver 8001`.
- **No se activa el entorno en PowerShell:** usa `.\.venv\Scripts\Activate.ps1`, CMD con `.\.venv\Scripts\activate.bat` o ejecuta directamente `.\.venv\Scripts\python.exe`.

Los ajustes actuales son para desarrollo. No despliegues estas aplicaciones directamente en producción; configura secretos y `DEBUG` de forma segura antes de cualquier despliegue.
