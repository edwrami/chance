"""
Configuración de Django para el proyecto ChancePro.
"""

import os
import socket
from pathlib import Path
from dotenv import load_dotenv

# =============================================================================
# CARGAR VARIABLES DE ENTORNO
# =============================================================================
load_dotenv()

# =============================================================================
# CONFIGURACIÓN BASE
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-chancepro-2024-seguro')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if host.strip()]

# =============================================================================
# APLICACIONES INSTALADAS
# =============================================================================
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Terceros
    'rest_framework',
    'corsheaders',
    
    # Nuestra app
    'core',
]

# =============================================================================
# MIDDLEWARE
# =============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================================================================
# URLS Y TEMPLATES
# =============================================================================
ROOT_URLCONF = 'chancepro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chancepro.wsgi.application'

# =============================================================================
# BASE DE DATOS - SUPABASE
# =============================================================================
import dj_database_url
import os



# Obtener la URL desde la variable de entorno
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Usar dj_database_url para parsear la URL
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
    # Forzar SSL
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
    print(f"✅ Conectando a Supabase")
else:
    # Fallback a SQLite si no hay DATABASE_URL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("⚠️ Usando SQLite local")

# =============================================================================
# MODELO DE USUARIO PERSONALIZADO
# =============================================================================
AUTH_USER_MODEL = 'core.Usuario'

# =============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# INTERNACIONALIZACIÓN
# =============================================================================
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# =============================================================================
# ARCHIVOS ESTÁTICOS Y MEDIA
# =============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =============================================================================
# CONFIGURACIÓN DE CAMPOS POR DEFECTO
# =============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CORS (Cross-Origin Resource Sharing)
# =============================================================================
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False') == 'True'
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if origin.strip()]

CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()]

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# =============================================================================
# DJANGO REST FRAMEWORK
# =============================================================================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# =============================================================================
# AUTENTICACIÓN Y LOGIN
# =============================================================================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

AUTHENTICATION_BACKENDS = [
    'core.authentication.DocumentoBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# =============================================================================
# CONFIGURACIÓN DE RED (IPv6)
# =============================================================================
# Forzar timeouts para conexiones de red
socket.setdefaulttimeout(30)

# NOTA: La personalización del admin se maneja en core/apps.py