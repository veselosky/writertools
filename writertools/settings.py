"""
Django settings for writertools project.

Generated by 'django-admin startproject'.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import importlib.util
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Get environment settings
env = environ.Env()
DOTENV = BASE_DIR / ".env"
if DOTENV.exists() and not env("IGNORE_ENV_FILE", default=False):
    environ.Env.read_env(DOTENV.open())

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "en-US"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

#######################################################################
# Integrations/Resources: settings likely to vary between environments
#######################################################################
# SECRET_KEY intentionally has no default, and will error if not provided
# in the environment. This ensures you don't accidentally run with an
# insecure configuration in production.
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", default=False)
MAIL_DEBUG = env("MAIL_DEBUG", default=DEBUG)
ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=[])

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
SQLITE_DB = BASE_DIR / "var" / "db.sqlite3"
DATABASES = {"default": env.db("DATABASE_URL", default=f"sqlite:///{SQLITE_DB}")}
CACHES = {"default": env.cache("CACHE_URL", default="locmemcache://")}
# Email settings don't use a dict. Add to local vars instead.
# https://django-environ.readthedocs.io/en/latest/#email-settings
EMAIL_CONFIG = env.email_url("EMAIL_URL", default="consolemail://")
vars().update(EMAIL_CONFIG)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "var" / "static"
if not STATIC_ROOT.exists():
    STATIC_ROOT.mkdir(parents=True, exist_ok=True)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "var" / "media"
if not MEDIA_ROOT.exists():
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache.
# See https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
if env("TESTING_MODE", default=False):
    # Prevents errors with different test runs stomping on each other's manifests
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
# But for production, you almost certainly should be using a shared storage backend, like:
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

# CELERY settings
# If the environment has not provided settings, assume there is no broker
# and run celery tasks in-process. This means you MUST provide
# CELERY_TASK_ALWAYS_EAGER=False in your environment to actually use celery.
CELERY_TASK_ALWAYS_EAGER = env("CELERY_TASK_ALWAYS_EAGER", default=True)
CELERY_TASK_EAGER_PROPAGATES = env("CELERY_TASK_EAGER_PROPAGATES", default=True)
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/7")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="")
CELERY_TIME_ZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


#######################################################################
# Application definition: typically same across all environments
#######################################################################
WSGI_APPLICATION = "writertools.wsgi.application"
ROOT_URLCONF = "writertools.urls"

INSTALLED_APPS = [
    "plotboard",
    "wordtracker",
    "genericsite",
    "django_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # 3rd party apps for genericsite
    "django_bootstrap_icons",
    "easy_thumbnails",
    "taggit",
    "tinymce",
    # Core Django below custom so we can override their templates
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    # https://docs.djangoproject.com/en/3.2/ref/middleware/#django.middleware.security.SecurityMiddleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # https://docs.djangoproject.com/en/3.2/ref/clickjacking/
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "genericsite.apps.context_defaults",
            ],
        },
    },
]

#######################################################################
# AUTHENTICATION
#######################################################################
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "writertools.auth.ProjectAuthAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_BLACKLIST = []  # TODO Will I need this?
ACCOUNT_USERNAME_VALIDATORS = None  # TODO Will I need this?

#######################################################################
# DEVELOPMENT: If running in a dev environment, loosen restrictions
# and add debugging tools.
#######################################################################
# Conditionally add django-extensions if it's installed
if importlib.util.find_spec("django_extensions"):
    INSTALLED_APPS.append("django_extensions")

if DEBUG:
    ALLOWED_HOSTS = ["*"]

    # Don't send email from dev environment, just write it to console.
    if MAIL_DEBUG:
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # Use the basic storage with no manifest
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

    if importlib.util.find_spec("debug_toolbar"):
        INSTALLED_APPS.append("debug_toolbar")
        MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
        INTERNAL_IPS = [
            "127.0.0.1",
        ]
        # See also urls.py for debug_toolbar urls
