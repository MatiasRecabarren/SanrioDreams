from pathlib import Path
import os
from django.contrib.messages import constants as messages_constants
import oracledb

try:
    connection = oracledb.connect(
        user='C##SanrioDreams',
        password='12345',
        dsn='localhost/XE'
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT BANNER FROM V$VERSION")
        version = cursor.fetchone()
        print("Versión de Oracle:", version[0])
except Exception as e:
    print("Error al conectar a Oracle:", str(e))

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-default-key')  # Usa un .env en producción
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps personalizadas
    'SitioWeb',
    'web',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs y WSGI
ROOT_URLCONF = 'web.urls'
WSGI_APPLICATION = 'web.wsgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Base de datos (usar PostgreSQL en producción)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'XE',  
        'USER': 'C##SanrioDreams',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '1521',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estáticos y media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Redirecciones
LOGIN_REDIRECT_URL = '/index'
LOGOUT_REDIRECT_URL = '/'

# Mensajes con Bootstrap
MESSAGE_TAGS = {
    messages_constants.DEBUG: 'alert-secondary',
    messages_constants.INFO: 'alert-info',
    messages_constants.SUCCESS: 'alert-success',
    messages_constants.WARNING: 'alert-warning',
    messages_constants.ERROR: 'alert-danger',
}

# Sesiones
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_SAVE_EVERY_REQUEST = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tuemail@gmail.com'  # Tu correo
EMAIL_HOST_PASSWORD = 'tu_app_password'  # Contraseña de aplicación de Google
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER