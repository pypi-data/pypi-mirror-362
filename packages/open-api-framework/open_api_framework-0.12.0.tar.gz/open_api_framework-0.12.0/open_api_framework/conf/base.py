import datetime
import os
import warnings
from pathlib import Path

from django.urls import reverse_lazy

import sentry_sdk
from corsheaders.defaults import default_headers as default_cors_headers
from log_outgoing_requests.formatters import HttpFormatter
from notifications_api_common.settings import *  # noqa

from .utils import (
    config,
    get_django_project_dir,
    get_project_dirname,
    get_sentry_integrations,
    strip_protocol_from_origin,
)

PROJECT_DIRNAME = get_project_dirname()

# Build paths inside the project, so further paths can be defined relative to
# the code root.
DJANGO_PROJECT_DIR = get_django_project_dir()
BASE_DIR = Path(DJANGO_PROJECT_DIR).resolve().parents[1]


#
# Core Django settings
#
SITE_ID = config(
    "SITE_ID",
    default=1,
    help_text="The database ID of the site object. You usually won't have to touch this.",
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY",
    help_text="Secret key that's used for certain cryptographic utilities. ",
)

# NEVER run with DEBUG=True in production-like environments
DEBUG = config(
    "DEBUG",
    default=False,
    help_text=(
        "Only set this to ``True`` on a local development environment. "
        "Various other security settings are derived from this setting!"
    ),
)

# = domains we're running on
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="",
    split=True,
    help_text=(
        "a comma separated (without spaces!) list of domains that serve "
        "the installation. Used to protect against Host header attacks."
    ),
    group="Required",
)
USE_X_FORWARDED_HOST = config(
    "USE_X_FORWARDED_HOST",
    default=False,
    help_text=(
        "whether to grab the domain/host from the X-Forwarded-Host header or not. "
        "This header is typically set by reverse proxies (such as nginx, traefik, Apache...). "
        "Note: this is a header that can be spoofed and you need to ensure you control it before enabling this."
    ),
)

IS_HTTPS = config(
    "IS_HTTPS",
    default=not DEBUG,
    help_text=(
        "Used to construct absolute URLs and controls a variety of security settings. "
        "Defaults to the inverse of ``DEBUG``."
    ),
    auto_display_default=False,
)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "nl-nl"

TIME_ZONE = "UTC"  # note: this *may* affect the output of DRF datetimes

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

#
# DATABASE and CACHING setup
#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config(
            "DB_NAME",
            PROJECT_DIRNAME,
            group="Database",
            help_text="name of the PostgreSQL database.",
        ),
        "USER": config(
            "DB_USER",
            PROJECT_DIRNAME,
            group="Database",
            help_text="username of the database user.",
        ),
        "PASSWORD": config(
            "DB_PASSWORD",
            PROJECT_DIRNAME,
            group="Database",
            help_text="password of the database user.",
        ),
        "HOST": config(
            "DB_HOST",
            "localhost",
            group="Database",
            help_text=(
                "hostname of the PostgreSQL database. Defaults to ``db`` for the docker environment, "
                "otherwise defaults to ``localhost``."
            ),
            auto_display_default=False,
        ),
        "PORT": config(
            "DB_PORT", 5432, group="Database", help_text="port number of the database"
        ),
    }
}

DATABASES["default"]["CONN_MAX_AGE"] = config(
    "DB_CONN_MAX_AGE",
    default=0,
    # The default is set to `60` in the docker settings, so that's what is mentioned
    # in the help text as well
    help_text=(
        "The lifetime of a database connection, as an integer of seconds. "
        "Use 0 to close database connections at the end of each request — Django’s historical behavior. "
        "This setting is ignored if connection pooling is used. Defaults to: ``60``."
    ),
    group="Database",
    auto_display_default=False,
    cast=lambda x: int(x) if x != "None" else None,
)

# https://docs.djangoproject.com/en/5.2/ref/databases/#connection-pool
# https://www.psycopg.org/psycopg3/docs/api/pool.html#the-connectionpool-class

DB_POOL_ENABLED = config(
    "DB_POOL_ENABLED",
    default=False,
    help_text=("Whether to use connection pooling."),
    group="Database",
)

DB_POOL_MIN_SIZE = config(
    "DB_POOL_MIN_SIZE",
    default=4,
    help_text=(
        "The minimum number of connection the pool will hold. "
        "The pool will actively try to create new connections if some are lost (closed, broken) "
        "and will try to never go below min_size."
    ),
    group="Database",
    cast=int,
)

DB_POOL_MAX_SIZE = config(
    "DB_POOL_MAX_SIZE",
    default=None,
    help_text=(
        "The maximum number of connections the pool will hold. "
        "If None, or equal to min_size, the pool will not grow or shrink. "
        "If larger than min_size, the pool can grow if more than min_size connections "
        "are requested at the same time and will shrink back after the extra connections "
        "have been unused for more than max_idle seconds."
    ),
    group="Database",
    cast=lambda x: int(x) if x is not None else None,
)

DB_POOL_TIMEOUT = config(
    "DB_POOL_TIMEOUT",
    default=30,
    help_text=(
        "The default maximum time in seconds that a client can wait "
        "to receive a connection from the pool (using connection() or getconn()). "
        "Note that these methods allow to override the timeout default."
    ),
    group="Database",
    cast=int,
)

DB_POOL_MAX_WAITING = config(
    "DB_POOL_MAX_WAITING",
    default=0,
    help_text=(
        "Maximum number of requests that can be queued to the pool, "
        "after which new requests will fail, raising TooManyRequests. 0 means no queue limit."
    ),
    group="Database",
    cast=int,
)

DB_POOL_MAX_LIFETIME = config(
    "DB_POOL_MAX_LIFETIME",
    default=60 * 60,
    help_text=(
        "The maximum lifetime of a connection in the pool, in seconds. "
        "Connections used for longer get closed and replaced by a new one. "
        "The amount is reduced by a random 10% to avoid mass eviction"
    ),
    group="Database",
    cast=int,
)

DB_POOL_MAX_IDLE = config(
    "DB_POOL_MAX_IDLE",
    default=10 * 60,
    help_text=(
        "Maximum time, in seconds, that a connection can stay unused in the pool "
        "before being closed, and the pool shrunk. This only happens to "
        "connections more than min_size, if max_size allowed the pool to grow."
    ),
    group="Database",
    cast=int,
)

DB_POOL_RECONNECT_TIMEOUT = config(
    "DB_POOL_RECONNECT_TIMEOUT",
    default=5 * 60,
    help_text=(
        "Maximum time, in seconds, the pool will try to create a connection. "
        "If a connection attempt fails, the pool will try to reconnect a few times, "
        "using an exponential backoff and some random factor to avoid mass attempts. "
        "If repeated attempts fail, after reconnect_timeout second the connection "
        "attempt is aborted and the reconnect_failed() callback invoked."
    ),
    group="Database",
    cast=int,
)

DB_POOL_NUM_WORKERS = config(
    "DB_POOL_NUM_WORKERS",
    default=3,
    help_text=(
        "Number of background worker threads used to maintain the pool state. "
        "Background workers are used for example to create new connections and "
        "to clean up connections when they are returned to the pool."
    ),
    group="Database",
    cast=int,
)


if DB_POOL_ENABLED:
    # FIXME Workaround for https://github.com/elastic/apm-agent-python/issues/2094
    # apm-agent-python does not instrument ConnectionPool yet
    import psycopg

    class WrapperConnectionClass(psycopg.Connection):
        @classmethod
        def connect(
            cls,
            conninfo: str = "",
            **kwargs,
        ) -> "psycopg.Connection[psycopg.rows.TupleRow]":
            return psycopg.connect(conninfo, **kwargs)

    DATABASES["default"]["OPTIONS"] = {
        "pool": {
            "min_size": DB_POOL_MIN_SIZE,
            "max_size": DB_POOL_MAX_SIZE,
            "timeout": DB_POOL_TIMEOUT,
            "max_waiting": DB_POOL_MAX_WAITING,
            "max_lifetime": DB_POOL_MAX_LIFETIME,
            "max_idle": DB_POOL_MAX_IDLE,
            "reconnect_timeout": DB_POOL_RECONNECT_TIMEOUT,
            "num_workers": DB_POOL_NUM_WORKERS,
            "connection_class": WrapperConnectionClass,
        }
    }
    # Cannot use a `CONN_MAX_AGE` other than 0 with connection pooling
    DATABASES["default"]["CONN_MAX_AGE"] = 0

# keep the current schema for now and deal with migrating to BigAutoField later, see
# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CACHE_DEFAULT = config(
    "CACHE_DEFAULT",
    "localhost:6379/0",
    help_text="redis cache address for the default cache (this **MUST** be set when using Docker)",
    group="Required",
)
CACHE_AXES = config(
    "CACHE_AXES",
    "localhost:6379/0",
    help_text=(
        "redis cache address for the brute force login protection cache "
        "(this **MUST** be set when using Docker)"
    ),
    group="Required",
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{CACHE_DEFAULT}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
    "axes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{CACHE_AXES}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
    "oidc": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{CACHE_DEFAULT}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
}

#
# APPLICATIONS enabled for this project
#
INSTALLED_APPS = [
    # Note: contenttypes should be first, see Django ticket #10827
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Optional applications.
    "django_admin_index",
    "ordered_model",
    "django.contrib.admin",
    # External applications.
    "axes",
    "django_filters",
    "csp",
    "corsheaders",
    "vng_api_common",
    "notifications_api_common",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "django_markup",
    "solo",
    # Two-factor authentication in the Django admin, enforced.
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "two_factor",
    "two_factor.plugins.webauthn",
    "maykin_2fa",
    "privates",
    "django_jsonform",
    "simple_certmanager",
    "zgw_consumers",
    "mozilla_django_oidc",
    "mozilla_django_oidc_db",
    "log_outgoing_requests",
    "django_setup_configuration",
    "sessionprofile",
    "open_api_framework",
    PROJECT_DIRNAME,
    # Django libraries
    "upgrade_check",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "sessionprofile.middleware.SessionProfileMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "maykin_2fa.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
    "csp.contrib.rate_limiting.RateLimitedCSPMiddleware",
]

ROOT_URLCONF = f"{PROJECT_DIRNAME}.urls"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path(DJANGO_PROJECT_DIR) / "templates"],
        "APP_DIRS": False,  # conflicts with explicity specifying the loaders
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "open_api_framework.context_processors.admin_settings",
                f"{PROJECT_DIRNAME}.utils.context_processors.settings",
            ],
            "loaders": TEMPLATE_LOADERS,
        },
    }
]

WSGI_APPLICATION = f"{PROJECT_DIRNAME}.wsgi.application"

# Translations
LOCALE_PATHS = (Path(DJANGO_PROJECT_DIR) / "conf" / "locale",)

#
# SERVING of static and media files
#

STATIC_URL = "/static/"

STATIC_ROOT = Path(BASE_DIR) / "static"

# Additional locations of static files
STATICFILES_DIRS = [Path(DJANGO_PROJECT_DIR) / "static"]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = Path(BASE_DIR) / "media"

MEDIA_URL = "/media/"

FILE_UPLOAD_PERMISSIONS = 0o644

#
# Sending EMAIL
#
EMAIL_HOST = config(
    "EMAIL_HOST",
    default="localhost",
    help_text="hostname for the outgoing e-mail server (this **MUST** be set when using Docker)",
    group="Required",
)
EMAIL_PORT = config(
    "EMAIL_PORT",
    default=25,
    help_text=(
        "port number of the outgoing e-mail server. Note that if you're on Google Cloud, "
        "sending e-mail via port 25 is completely blocked and you should use 487 for TLS."
    ),
)  # disabled on Google Cloud, use 487 instead
EMAIL_HOST_USER = config(
    "EMAIL_HOST_USER", default="", help_text="username to connect to the mail server"
)
EMAIL_HOST_PASSWORD = config(
    "EMAIL_HOST_PASSWORD",
    default="",
    help_text="password to connect to the mail server",
)
EMAIL_USE_TLS = config(
    "EMAIL_USE_TLS",
    default=False,
    help_text=(
        "whether to use TLS or not to connect to the mail server. "
        "Should be True if you're changing the ``EMAIL_PORT`` to 487."
    ),
)
EMAIL_TIMEOUT = 10

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    f"{PROJECT_DIRNAME}@example.com",
    help_text="The default email address from which emails are sent",
)

#
# LOGGING
#
LOG_STDOUT = config(
    "LOG_STDOUT",
    default=True,
    help_text="whether to log to stdout or not",
    group="Logging",
)
LOG_LEVEL = config(
    "LOG_LEVEL",
    default="INFO",
    help_text=(
        "control the verbosity of logging output. "
        "Available values are ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO`` and ``DEBUG``"
    ),
    group="Logging",
)
LOG_QUERIES = config(
    "LOG_QUERIES",
    default=False,
    help_text=(
        "enable (query) logging at the database backend level. Note that you "
        "must also set ``DEBUG=1``, which should be done very sparingly!"
    ),
    group="Logging",
)
# XXX: this should be renamed to `LOG_OUTGOING_REQUESTS` in the next major release
LOG_REQUESTS = config(
    "LOG_REQUESTS",
    default=False,
    help_text=(
        "enable logging of the outgoing requests. "
        "This must be enabled along with `LOG_OUTGOING_REQUESTS_DB_SAVE` to save outgoing request logs in the database."
    ),
    group="Logging",
)
if LOG_QUERIES and not DEBUG:
    warnings.warn(
        "Requested LOG_QUERIES=1 but DEBUG is false, no query logs will be emited.",
        RuntimeWarning,
    )

CELERY_LOGLEVEL = config(
    "CELERY_LOGLEVEL",
    default="INFO",
    help_text="control the verbosity of logging output for celery, independent of ``LOG_LEVEL``."
    " Available values are ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO`` and ``DEBUG``",
    group="Celery",
)

LOGGING_DIR = Path(BASE_DIR) / "log"

logging_root_handlers = ["console"] if LOG_STDOUT else ["project"]
logging_django_handlers = ["console"] if LOG_STDOUT else ["django"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(name)s %(module)s %(process)d %(thread)d  %(message)s"
        },
        "timestamped": {"format": "%(asctime)s %(levelname)s %(name)s  %(message)s"},
        "simple": {"format": "%(levelname)s  %(message)s"},
        "performance": {"format": "%(asctime)s %(process)d | %(thread)d | %(message)s"},
        "db": {"format": "%(asctime)s | %(message)s"},
        "outgoing_requests": {"()": HttpFormatter},
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "timestamped",
        },
        "console_db": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "db",
        },
        "celery_console": {
            "level": CELERY_LOGLEVEL,
            "class": "logging.StreamHandler",
            "formatter": "timestamped",
        },
        "celery_file": {
            "level": CELERY_LOGLEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "celery.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "django": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "django.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "project": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / f"{PROJECT_DIRNAME}.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "performance": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "performance.log",
            "formatter": "performance",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "requests": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGGING_DIR) / "requests.log",
            "formatter": "timestamped",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 10,
        },
        "log_outgoing_requests": {
            "level": "DEBUG",
            "formatter": "outgoing_requests",
            "class": "logging.StreamHandler",  # to write to stdout
        },
        "save_outgoing_requests": {
            "level": "DEBUG",
            # enabling saving to database
            "class": "log_outgoing_requests.handlers.DatabaseOutgoingRequestsHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": logging_root_handlers,
            "level": "ERROR",
            "propagate": False,
        },
        PROJECT_DIRNAME: {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "mozilla_django_oidc": {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
        },
        f"{PROJECT_DIRNAME}.utils.middleware": {
            "handlers": logging_root_handlers,
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "vng_api_common": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["console_db"] if LOG_QUERIES else [],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": logging_django_handlers,
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django.template": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "log_outgoing_requests": {
            "handlers": (
                ["log_outgoing_requests", "save_outgoing_requests"]
                if LOG_REQUESTS
                else []
            ),
            "level": "DEBUG",
            "propagate": True,
        },
        "celery": {
            "handlers": ["celery_console"] if LOG_STDOUT else ["celery_file"],
            "level": CELERY_LOGLEVEL,
            "propagate": True,
        },
    },
}

#
# AUTH settings - user accounts, passwords, backends...
#
AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Allow logging in with both username+password and email+password
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    f"{PROJECT_DIRNAME}.accounts.backends.UserModelEmailBackend",
    "django.contrib.auth.backends.ModelBackend",
    "mozilla_django_oidc_db.backends.OIDCAuthenticationBackend",
]

SESSION_COOKIE_NAME = f"{PROJECT_DIRNAME}_sessionid"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_COOKIE_AGE = config(
    "SESSION_COOKIE_AGE",
    default=1209600,
    help_text="For how long, in seconds, the session cookie will be valid.",
)

LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = reverse_lazy("admin:index")
LOGOUT_REDIRECT_URL = reverse_lazy("admin:index")

#
# SECURITY settings
#
SESSION_COOKIE_SECURE = IS_HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = config(
    "SESSION_COOKIE_SAMESITE",
    "Lax",
    help_text=(
        "The value of the SameSite flag on the session cookie. This flag prevents the "
        "cookie from being sent in cross-site requests thus preventing CSRF attacks and "
        "making some methods of stealing session cookie impossible."
        "Currently interferes with OIDC. Keep the value set at Lax if used."
    ),
)

CSRF_COOKIE_SECURE = IS_HTTPS
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = config(
    "CSRF_COOKIE_SAMESITE",
    "Strict",
    help_text=(
        "The value of the SameSite flag on the CSRF cookie. This flag prevents the cookie "
        "from being sent in cross-site requests."
    ),
)

if IS_HTTPS:
    SECURE_HSTS_SECONDS = 31536000

X_FRAME_OPTIONS = "DENY"

#
# Silenced checks
#
SILENCED_SYSTEM_CHECKS = [
    "rest_framework.W001",
    "debug_toolbar.W006",
]


#
# Increase number of parameters for GET/POST requests
#
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

#
# Custom settings
#
ENVIRONMENT = config(
    "ENVIRONMENT",
    "",
    help_text=(
        "An identifier for the environment, displayed in the admin depending on "
        "the settings module used and included in the error monitoring (see ``SENTRY_DSN``). "
        "The default is set according to ``DJANGO_SETTINGS_MODULE``."
    ),
    auto_display_default=False,
)
ENVIRONMENT_SHOWN_IN_ADMIN = True

# Generating the schema, depending on the component
subpath = config(
    "SUBPATH",
    None,
    help_text=(
        "If hosted on a subpath, provide the value here. If you provide ``/gateway``, "
        "the component assumes its running at the base URL: ``https://somedomain/gateway/``. "
        "Defaults to an empty string."
    ),
)
if subpath:
    if not subpath.startswith("/"):
        subpath = f"/{subpath}"
    SUBPATH = subpath

if "GIT_SHA" in os.environ:
    GIT_SHA = config("GIT_SHA", "", add_to_docs=False)
# in docker (build) context, there is no .git directory
elif (Path(BASE_DIR) / ".git").exists():
    try:
        import git
    except ImportError:
        GIT_SHA = None
    else:
        repo = git.Repo(search_parent_directories=True)
        GIT_SHA = repo.head.object.hexsha
else:
    GIT_SHA = None

RELEASE = config(
    "RELEASE",
    GIT_SHA,
    help_text="The version number or commit hash of the application (this is also sent to Sentry).",
    auto_display_default=False,
)

NUM_PROXIES = config(  # TODO: this also is relevant for DRF settings if/when we have rate-limited endpoints
    "NUM_PROXIES",
    default=1,
    cast=lambda val: int(val) if val is not None else None,
    help_text=(
        "the number of reverse proxies in front of the application, as an integer. "
        "This is used to determine the actual client IP adres. "
        "On Kubernetes with an ingress you typically want to set this to 2."
    ),
)

##############################
#                            #
# 3RD PARTY LIBRARY SETTINGS #
#                            #
##############################

#
# DJANGO-AXES (6.0+)
#
AXES_CACHE = "axes"  # refers to CACHES setting
# The number of login attempts allowed before a record is created for the
# failed logins. Default: 3
AXES_FAILURE_LIMIT = 5
AXES_LOCK_OUT_AT_FAILURE = True  # Default: True
# If set, defines a period of inactivity after which old failed login attempts
# will be forgotten. Can be set to a python timedelta object or an integer. If
# an integer, will be interpreted as a number of hours. Default: None
AXES_COOLOFF_TIME = datetime.timedelta(minutes=5)
# The number of reverse proxies
AXES_IPWARE_PROXY_COUNT = NUM_PROXIES - 1 if NUM_PROXIES else None
# If set, specifies a template to render when a user is locked out. Template
# receives cooloff_time and failure_limit as context variables. Default: None
AXES_LOCKOUT_TEMPLATE = "account_blocked.html"
AXES_LOCKOUT_PARAMETERS = [["ip_address", "user_agent", "username"]]
AXES_BEHIND_REVERSE_PROXY = IS_HTTPS
# By default, Axes obfuscates values for formfields named "password", but the admin
# interface login formfield name is "auth-password", so we want to obfuscate that
AXES_SENSITIVE_PARAMETERS = ["password", "auth-password"]  # nosec

# The default meta precedence order
IPWARE_META_PRECEDENCE_ORDER = (
    "HTTP_X_FORWARDED_FOR",
    "X_FORWARDED_FOR",  # <client>, <proxy1>, <proxy2>
    "HTTP_CLIENT_IP",
    "HTTP_X_REAL_IP",
    "HTTP_X_FORWARDED",
    "HTTP_X_CLUSTER_CLIENT_IP",
    "HTTP_FORWARDED_FOR",
    "HTTP_FORWARDED",
    "HTTP_VIA",
    "REMOTE_ADDR",
)

#
# DJANGO-CORS-MIDDLEWARE
#
CORS_ALLOW_ALL_ORIGINS = config(
    "CORS_ALLOW_ALL_ORIGINS",
    default=False,
    group="Cross-Origin-Resource-Sharing",
    help_text="allow cross-domain access from any client",
)
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    split=True,
    default=[],
    group="Cross-Origin-Resource-Sharing",
    help_text=(
        "explicitly list the allowed origins for cross-domain requests. "
        "Example: http://localhost:3000,https://some-app.gemeente.nl"
    ),
)
CORS_ALLOWED_ORIGIN_REGEXES = config(
    "CORS_ALLOWED_ORIGIN_REGEXES",
    split=True,
    default=[],
    group="Cross-Origin-Resource-Sharing",
    help_text="same as ``CORS_ALLOWED_ORIGINS``, but supports regular expressions",
)
# Authorization is included in default_cors_headers
CORS_ALLOW_HEADERS = (
    list(default_cors_headers)
    + [
        "accept-crs",
        "content-crs",
    ]
    + config(
        "CORS_EXTRA_ALLOW_HEADERS",
        split=True,
        default=[],
        group="Cross-Origin-Resource-Sharing",
        help_text=(
            "headers that are allowed to be sent as part of the cross-domain request. "
            "By default, Authorization, Accept-Crs and Content-Crs are already included. "
            "The value of this variable is added to these already included headers."
        ),
    )
)
CORS_EXPOSE_HEADERS = [
    "content-crs",
]
# Django's SESSION_COOKIE_SAMESITE = "Lax" prevents session cookies from being sent
# cross-domain. There is no need for these cookies to be sent, since the API itself
# uses Bearer Authentication.
# we can't easily derive this from django-cors-headers, see also
# https://pypi.org/project/django-cors-headers/#csrf-integration
#
# So we do a best effort attempt at re-using configuration parameters, with an escape
# hatch to override it.
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    split=True,
    default=[strip_protocol_from_origin(origin) for origin in CORS_ALLOWED_ORIGINS],
    help_text="A list of trusted origins for unsafe requests (e.g. POST)",
)
#
# DJANGO-PRIVATES -- safely serve files after authorization
#
PRIVATE_MEDIA_ROOT = Path(BASE_DIR) / "private-media"
PRIVATE_MEDIA_URL = "/private-media/"


#
# NOTIFICATIONS-API-COMMON
#
NOTIFICATIONS_DISABLED = config(
    "NOTIFICATIONS_DISABLED",
    default=False,
    help_text=(
        "indicates whether or not notifications should be sent to the Notificaties API "
        "for operations on the API endpoints. "
        "Defaults to ``True`` for the ``dev`` environment, otherwise defaults to ``False``"
    ),
    auto_display_default=False,
)
SITE_DOMAIN = config(
    "SITE_DOMAIN",
    default="",
    help_text=("Defines the primary domain where the application is hosted."),
)

#
# SENTRY - error monitoring
#
SENTRY_DSN = config(
    "SENTRY_DSN",
    None,
    help_text=(
        "URL of the sentry project to send error reports to. Default empty, "
        "i.e. -> no monitoring set up. Highly recommended to configure this."
    ),
    auto_display_default=False,
)

if SENTRY_DSN:
    SENTRY_CONFIG = {
        "dsn": SENTRY_DSN,
        "release": RELEASE or "RELEASE not set",
        "environment": ENVIRONMENT,
    }

    sentry_sdk.init(
        **SENTRY_CONFIG,
        integrations=get_sentry_integrations(),
        send_default_pii=True,
    )


#
# CELERY
#
CELERY_BROKER_URL = config(
    "CELERY_RESULT_BACKEND",
    "redis://localhost:6379/1",
    group="Celery",
    help_text="the URL of the backend/broker that will be used by Celery to send the notifications",
)
CELERY_RESULT_BACKEND = config(
    "CELERY_RESULT_BACKEND",
    "redis://localhost:6379/1",
    group="Celery",
    help_text="the URL of the backend/broker that will be used by Celery to send the notifications",
)


#
# DJANGO-ADMIN-INDEX
#
ADMIN_INDEX_SHOW_REMAINING_APPS_TO_SUPERUSERS = False
ADMIN_INDEX_AUTO_CREATE_APP_GROUP = False

#
# Mozilla Django OIDC DB settings
#
OIDC_AUTHENTICATE_CLASS = "mozilla_django_oidc_db.views.OIDCAuthenticationRequestView"
# Use custom callback view to handle admin login error situations
# NOTE the AdminLoginFailure view for mozilla-django-oidc-db should be added to the projects
# urlpatterns to properly catch errors
OIDC_CALLBACK_CLASS = "mozilla_django_oidc_db.views.OIDCCallbackView"
MOZILLA_DJANGO_OIDC_DB_CACHE = "oidc"
MOZILLA_DJANGO_OIDC_DB_CACHE_TIMEOUT = 5 * 60

#
# Elastic APM
#
ELASTIC_APM_SERVER_URL = config(
    "ELASTIC_APM_SERVER_URL",
    None,
    help_text="URL where Elastic APM is hosted",
    group="Elastic APM",
)
ELASTIC_APM = {
    # FIXME this does change the default service name, because PROJECT_DIRNAME != PROJECT_NAME
    "SERVICE_NAME": config(
        "ELASTIC_APM_SERVICE_NAME",
        f"{PROJECT_DIRNAME} - {ENVIRONMENT}",
        help_text=(
            f"Name of the service for this application in Elastic APM. "
            f"Defaults to ``{PROJECT_DIRNAME} - <environment>``"
        ),
        group="Elastic APM",
        auto_display_default=False,
    ),
    "SECRET_TOKEN": config(
        "ELASTIC_APM_SECRET_TOKEN",
        "default",
        help_text="Token used to communicate with Elastic APM",
        group="Elastic APM",
    ),
    "SERVER_URL": ELASTIC_APM_SERVER_URL,
    "TRANSACTION_SAMPLE_RATE": config(
        "ELASTIC_APM_TRANSACTION_SAMPLE_RATE",
        0.1,
        help_text=(
            "By default, the agent will sample every transaction (e.g. request to your service). "
            "To reduce overhead and storage requirements, set the sample rate to a value between 0.0 and 1.0"
        ),
        group="Elastic APM",
    ),
}
if not ELASTIC_APM_SERVER_URL:
    ELASTIC_APM["ENABLED"] = False
    ELASTIC_APM["SERVER_URL"] = "http://localhost:8200"
else:
    MIDDLEWARE = ["elasticapm.contrib.django.middleware.TracingMiddleware"] + MIDDLEWARE
    INSTALLED_APPS = INSTALLED_APPS + [
        "elasticapm.contrib.django",
    ]


#
# MAYKIN-2FA
# Uses django-two-factor-auth under the hood, so relevant upstream package settings
# apply too.
#

# we run the admin site monkeypatch instead.
TWO_FACTOR_PATCH_ADMIN = False
# Relying Party name for WebAuthn (hardware tokens)
TWO_FACTOR_WEBAUTHN_RP_NAME = f"{PROJECT_DIRNAME} - admin"
# use platform for fingerprint readers etc., or remove the setting to allow any.
# cross-platform would limit the options to devices like phones/yubikeys
TWO_FACTOR_WEBAUTHN_AUTHENTICATOR_ATTACHMENT = "cross-platform"
# add entries from AUTHENTICATION_BACKENDS that already enforce their own two-factor
# auth, avoiding having some set up MFA again in the project.
MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = [
    "mozilla_django_oidc_db.backends.OIDCAuthenticationBackend",
]

# if DISABLE_2FA is true, fill the MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS with all
# configured AUTHENTICATION_BACKENDS and thus disabeling the entire 2FA chain.
if config(
    "DISABLE_2FA",
    default=False,
    help_text="Whether or not two factor authentication should be disabled",
):  # pragma: no cover
    MAYKIN_2FA_ALLOW_MFA_BYPASS_BACKENDS = AUTHENTICATION_BACKENDS


#
# LOG OUTGOING REQUESTS
#
LOG_OUTGOING_REQUESTS_EMIT_BODY = config(
    "LOG_OUTGOING_REQUESTS_EMIT_BODY",
    default=True,
    help_text="Whether or not outgoing request bodies should be logged",
    group="Logging",
)
LOG_OUTGOING_REQUESTS_DB_SAVE = config(
    "LOG_OUTGOING_REQUESTS_DB_SAVE",
    default=False,
    help_text="Whether or not outgoing request logs should be saved to the database",
    group="Logging",
)
LOG_OUTGOING_REQUESTS_DB_SAVE_BODY = config(
    "LOG_OUTGOING_REQUESTS_DB_SAVE_BODY",
    default=True,
    help_text="Whether or not outgoing request bodies should be saved to the database",
    group="Logging",
)
LOG_OUTGOING_REQUESTS_RESET_DB_SAVE_AFTER = None
LOG_OUTGOING_REQUESTS_MAX_AGE = config(
    "LOG_OUTGOING_REQUESTS_MAX_AGE",
    default=7,
    help_text="The amount of time after which request logs should be deleted from the database",
    group="Logging",
)  # number of days


#
# Django CSP settings
#
# explanation of directives: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
# and how to specify them: https://django-csp.readthedocs.io/en/latest/configuration.html
#
# NOTE: make sure values are a tuple or list, and to quote special values like 'self'

# ideally we'd use BASE_URI but it'd have to be lazy or cause issues
CSP_DEFAULT_SRC = ["'self'"] + config(
    "CSP_EXTRA_DEFAULT_SRC",
    default=[],
    split=True,
    group="Content Security Policy",
    help_text="Extra default source URLs for CSP other than ``self``. "
    "Used for ``img-src``, ``style-src`` and ``script-src``",
)


CSP_REPORT_URI = config(
    "CSP_REPORT_URI",
    None,
    group="Content Security Policy",
    help_text="URI of the``report-uri`` directive.",
)
CSP_REPORT_PERCENTAGE = config(
    "CSP_REPORT_PERCENTAGE",
    0,
    group="Content Security Policy",
    help_text="Percentage of requests that get the ``report-uri`` directive.",
)  # float between 0 and 1

CSP_FORM_ACTION = (
    config(
        "CSP_FORM_ACTION",
        default=["\"'self'\""]
        + config(
            "CSP_EXTRA_FORM_ACTION",
            default=[],
            split=True,
            group="Content Security Policy",
            help_text="Add additional ``form-action`` source to the default ",
        ),
        split=True,
        group="Content Security Policy",
        help_text="Override the default ``form-action`` source",
    )
    + CORS_ALLOWED_ORIGINS
)

CSP_IMG_SRC = (
    CSP_DEFAULT_SRC
    + ["data:", "cdn.redoc.ly"]  # used by DRF spectacular
    + config(
        "CSP_EXTRA_IMG_SRC",
        default=[],
        split=True,
        group="Content Security Policy",
        help_text="Extra ``img-src`` sources for CSP other than ``CSP_DEFAULT_SRC``.",
    )
)

# affects <object> and <embed> tags, block everything by default but allow deploy-time
# overrides.
CSP_OBJECT_SRC = config(
    "CSP_OBJECT_SRC",
    default=["\"'none'\""],
    split=True,
    group="Content Security Policy",
    help_text="``object-src`` urls",
)

# we must include this explicitly, otherwise the style-src only includes the nonce because
# of CSP_INCLUDE_NONCE_IN
CSP_STYLE_SRC = CSP_DEFAULT_SRC + [
    "'unsafe-inline'",
    "fonts.googleapis.com",
]  # used by DRF spectacular
CSP_SCRIPT_SRC = CSP_DEFAULT_SRC + ["'unsafe-inline'"]
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com")
CSP_WORKER_SRC = ("'self'", "blob:")

# firefox does not get the nonce from default-src, see
# https://stackoverflow.com/a/63376012
CSP_INCLUDE_NONCE_IN = ["style-src", "script-src"]

# directives that don't fallback to default-src
CSP_BASE_URI = ["'self'"]

# Frame directives do not fall back to default-src
CSP_FRAME_ANCESTORS = ["'none'"]  # equivalent to X-Frame-Options: deny
CSP_FRAME_SRC = ["'self'"]
# CSP_NAVIGATE_TO = ["'self'"]  # this will break all outgoing links etc  # too much & tricky, see note on MDN
# CSP_SANDBOX # too much

CSP_UPGRADE_INSECURE_REQUESTS = False  # TODO enable on production?


#
# Django Solo
#
SOLO_CACHE = "default"
