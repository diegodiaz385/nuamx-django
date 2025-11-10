"""
Django settings for core project – listo para NUAMX (Plantillas + DRF + SQLite + .env).

- Variables desde .env (SECRET_KEY, DEBUG, ALLOWED_HOSTS).
- Templates en web/templates/
- Estáticos en web/static/
- Base de datos: SQLite por defecto (simple y sin credenciales).
- DRF con JWT (SimpleJWT) listo.
"""

from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables del archivo .env en la raíz del proyecto
load_dotenv(BASE_DIR / ".env")

# Seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
DEBUG = os.getenv("DEBUG", "True").strip().lower() == "true"
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

# Apps instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "rest_framework",
    # "rest_framework_simplejwt",  # no es obligatorio registrarla como app
    # Apps del proyecto
    "api",
    "web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

# Templates: buscamos en web/templates además de las carpetas templates de las apps
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "web" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Base de datos: forzamos SQLite (evita DPY-4001)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Cortafuegos por si alguna variable intenta forzar otra DB
for var in ("DATABASE_URL", "DB_ENGINE", "ORACLE_USER", "ORACLE_PASSWORD", "ORACLE_DSN"):
    os.environ.pop(var, None)

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localización
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# Archivos estáticos y media
STATIC_URL = "/static/"
# ⬇️ Mantiene tu carpeta raiz de estáticos (sirve /static/js/reportes_botones.js)
STATICFILES_DIRS = [BASE_DIR / "web" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ⬇️ Finders explícitos para que CalificacionTemplateView pueda usar `finders.find()`
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# DRF + JWT listo para usar con SimpleJWT
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Clave por defecto de PK
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
