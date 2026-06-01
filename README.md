# ChancePro

Sistema Django para gestión de apuestas, loterías, chanceros, empresarios, reportes y topes de premio.

## Requisitos

- Python 3.11+
- PostgreSQL/Supabase para producción
- pip

## Instalación local

1. Crear entorno virtual:

```bash
python -m venv .venv
```

2. Activar entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear archivo `.env` desde el ejemplo:

```bash
copy .env.example .env
```

5. Configurar variables en `.env`.

Para desarrollo local puedes dejar `DATABASE_URL` vacío y se usará SQLite.

6. Ejecutar migraciones:

```bash
python manage.py migrate
```

7. Crear superusuario:

```bash
python manage.py createsuperuser
```

8. Ejecutar servidor local:

```bash
python manage.py runserver
```

## Variables de entorno

```env
SECRET_KEY=change-this-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=
CSRF_TRUSTED_ORIGINS=
SECURE_SSL_REDIRECT=True
```

## Producción

En producción configura:

```env
DEBUG=False
SECRET_KEY=una-clave-segura
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=postgresql://usuario:password@host:puerto/dbname
CSRF_TRUSTED_ORIGINS=https://tudominio.com,https://www.tudominio.com
CORS_ALLOW_ALL_ORIGINS=False
SECURE_SSL_REDIRECT=True
```

## Comandos de despliegue

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn chancepro.wsgi:application
```

## Archivos importantes

- `Procfile`: comando para plataformas tipo Render/Heroku.
- `runtime.txt`: versión sugerida de Python.
- `.env.example`: plantilla de variables de entorno.
- `.gitignore`: evita subir secretos, base local, estáticos generados y archivos temporales.

## Subir a GitHub

```bash
git init
git add .
git commit -m "Preparar proyecto para despliegue"
git branch -M main
git remote add origin https://github.com/edwrami/chance.git
git push -u origin main
```

**Importante:** nunca subas el archivo `.env` real. Solo sube `.env.example`.

## Repositorio oficial

```bash
https://github.com/edwrami/chance.git
```

## Claves reales en servidor

Las claves reales no deben quedar guardadas en GitHub. Configúralas directamente en el servidor como variables de entorno:

```env
SECRET_KEY=clave-real-segura
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgresql://usuario:password@host:puerto/dbname
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://tu-dominio.com
SECURE_SSL_REDIRECT=True
```
