from importlib import import_module

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase


def get_session_store() -> SessionBase:
    return import_module(settings.SESSION_ENGINE).SessionStore
