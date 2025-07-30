Changelog
=========

0.12.0 (2025-07-15)
-------------------

**💥 Breaking changes**

* Specify optional dependency groups:

    * **celery**: ``celery``, ``flower``
    * **cors**: ``django-cors-headers``
    * **markup**: ``django-markup``
    * **geo**: ``djangorestframework-gis``
    * **csp**: ``django-csp``
    * **commonground**: ``commonground-api-common``
    * **inclusions**: ``djangorestframework-inclusions``
    * **sanitization**: ``bleach``
    * **server**: ``uwsgi``
    * **redis**: ``django-redis``

**New features**

* Add DB connection pooling envvars + configuration (with workaround to make sure it works with APM)

    * ``DB_POOL_ENABLED``
    * ``DB_POOL_MIN_SIZE``
    * ``DB_POOL_MAX_SIZE``
    * ``DB_POOL_TIMEOUT``
    * ``DB_POOL_MAX_WAITING``
    * ``DB_POOL_MAX_LIFETIME``
    * ``DB_POOL_MAX_IDLE``
    * ``DB_POOL_RECONNECT_TIMEOUT``
    * ``DB_POOL_NUM_WORKERS``

* Add ``DB_CONN_MAX_AGE`` envvar (automatically set to 0 if connection pooling is enabled)

**Maintenance**

* Pin ```commonground-api-common``` to 2.7.0 or higher

0.11.0 (2025-07-03)
-------------------

**New features**

* Replace ``psycopg2`` with ``psycopg[binary]`` to support connection pooling

0.10.3 (2025-06-17)
-------------------

**Bugfixes**

* [maykinmedia/objects-api#620] Change ``LOG_LEVEL`` environment variable default value from ``WARNING`` to ``INFO``

0.10.2 (2025-06-11)
-------------------

**New features**

* [#139] Add ``django-upgrade-check`` dependency and set Python 3.12 as the minimum required version

0.10.1 (2025-05-26)
-------------------

**Bugfixes**

* Do not use ``save_outgoing_requests`` log handler if ``LOG_REQUESTS`` is set to false

**Maintenance**

* [#132] Replace ``check_sphinx.py`` with ``make``
* [#133] Replace ``black``, ``isort`` and ``flake8`` with ``ruff`` and update code-quality workflow
* [#140] Upgrade python to 3.12
* Upgrade codecov action to v4


0.10.0 (2025-05-19)
-------------------

**New features**

* Add separate "Logging" group for logging related environment variables in docs
* Add ``open_api_framework.conf.utils.mute_logging`` util to silence logging in CI
* [maykinmedia/objects-api#592] Silence log events in Sentry if structlog is used

**Bugfixes**

* [#127] Make ``LOGIN_URL`` non-lazy to avoid errors when using ``django-rosetta``

0.9.6 (2025-03-28)
------------------

**Maintenance**

* [#59] Set ``SITE_DOMAIN`` default to an empty string and add ``SITE_ID``


0.9.5 (2025-03-24)
------------------

**Maintenance**

* [#open-zaak/open-zaak#1856] Allow Django 5 as a dependency.


0.9.4 (2025-03-20)
------------------

**Maintenance**

* [#59] Remove ``django.contrib.sites`` dependency and add ``SITE_DOMAIN`` environment variable


0.9.3 (2025-02-24)
------------------

**Bugfixes**

* [#88] Automatically initialize Sentry when importing base settings and expose ``SENTRY_CONFIG`` setting

    .. warning::

        The ``init_sentry`` function was removed and now Sentry is initialized immediately in
        ``open_api_framework/conf/base.py``. If your project requires additional parameters
        to be specified (e.g. a ``before_send`` hook), it is best to reinitialize Sentry manually in your project's base setting:

        .. code-block:: python

            from open_api_framework.conf.base import *  # noqa
            from open_api_framework.conf.utils import get_sentry_integrations

            from your_project.utils import before_send_hook

            # Reinitialize Sentry to add the before_send hook
            SENTRY_CONFIG["before_send"] = before_send_hook
            sentry_sdk.init(
                **SENTRY_CONFIG,
                integrations=get_sentry_integrations(),
                send_default_pii=True,
            )


**Maintenance**

* [#90] bump commonground api version to 2.1.2

**Documentation**

* [#108] Mention in docs that importing anything from ``base.py`` causes all settings to be loaded


0.9.2 (2025-01-02)
------------------

**Security updates**

* Upgrade django to 4.2.17

0.9.1 (2024-12-16)
------------------

**Bugfixes/QOL**

* Change ``LOG_STDOUT`` default value to True
* Re-add separate ``CELERY_LOGLEVEL`` configuration setting


0.9.0 (2024-11-11)
------------------
**New Features**

* Add ``SESSION_COOKIE_AGE`` configurable setting
* Add user session management admin

.. note::

 SessionProfile admin should be added to admin index and its fixture.

**Bugfixes/QOL**

* fix runtime configuration for django-log-outgoing-requests

0.8.1 (2024-09-26)
------------------

**Bugfixes/QOL**

* Change SESSION_COOKIE_SAMESITE to "Lax" to fix OIDC (#72)
* Remove url from SECRET_KEY help text (#76)
* Change CSP headers to support API schema page

0.8.0 (2024-08-22)
------------------

**New features**

* Add Django CSP with configurable settings
* Add SECURE_HSTS_SECONDS and CSRF_COOKIE_HTTPONLY settings

.. warning::

    SECURE_HSTS_SECONDS has been added with a default of 31536000 seconds, ensure that
    before upgrading to this version of open-api-framework, your entire application is served
    over HTTPS, otherwise this setting can break parts of your application (see https://docs.djangoproject.com/en/4.2/ref/middleware/#http-strict-transport-security)

**Bugfixes/QOL**

* Fix rendering for envvar defaults (previously quotes were escaped)
* Move ``CACHE_DEFAULT``, ``CACHE_AXES``, ``EMAIL_HOST`` envvars to Required group (because they are required for Docker)
* Add CI job to check if all envvars are either documented or excluded from documentation

0.7.1 (2024-08-16)
------------------

**Bugfixes**

* Add missing help_text for SESSION_COOKIE_SAMESITE and CSRF_COOKIE_SAMESITE envvars

0.7.0 (2024-08-15)
------------------

**New features**

* Management command to generate documentation for environment variables
* Made SESSION_COOKIE_SAMESITE and CSRF_COOKIE_SAMESITE configurable via environment variables (default ``Strict``)

0.6.1 (2024-07-31)
------------------

**Project maintenance and QOL**

* Updated dependencies:
    - django ``4.2.11+`` to ``4.2.14+``
    - django-axes ``6.3.0+`` to ``6.5.1+``
    - django-cors-headers ``4.3.1+`` to ``4.4.0+``
    - django-jsonform ``2.21.4+`` to ``2.22.0+``
    - djangorestframework ``3.12.4+`` to ``3.15.2+``
    - django-filter ``23.2+`` to ``24.2+``
    - drf-spectacular ``0.27.0+`` to ``0.27.2+``
    - mozilla-django-oidc-db ``0.14.1+`` to ``0.19.0+``
    - requests ``2.31.0+`` to ``2.32.3+``
    - sentry-sdk ``1.39.2+`` to ``2.11.0+``
    - elastic-apm ``6.20.0+`` to ``6.22.0+``
    - celery ``5.2.7+`` to ``5.4.0+``
    - maykin-2fa ``1.0.0+`` to ``1.0.1+``


0.6.0 (2024-07-04)
------------------

**New features**

* Use the callback class from mozilla-django-oidc-db to allow for a custom error view

0.5.0 (2024-06-27)
------------------

**New features**

* Add password to ``AXES_SENSITIVE_PARAMETERS``
* Use stricter ``django-axes`` settings
    * ``AXES_FAILURE_LIMIT`` changed from ``10`` to ``5``
    * ``AXES_COOLOFF_TIME`` changed from ``1`` to ``5`` minutes
* Make more ``log-outgoing-requests`` settings configurable
    * ``LOG_OUTGOING_REQUESTS_EMIT_BODY`` (default ``True``)
    * ``LOG_OUTGOING_REQUESTS_DB_SAVE_BODY`` (default ``True``)
* Add base template to display current version in admin

**Bugfixes**

* Remove FIXTURE_DIRS setting and add root level app to INSTALLED_APPS

**Other**

* Move documentation to readthedocs

0.4.2 (2024-06-20)
------------------

**Bugfixes**

* Add missing settings for ``TWO_FACTOR_WEBAUTHN``

0.4.1 (2024-06-13)
------------------

**Bugfixes**

* Add ``ordered_model`` to ``INSTALLED_APPS`` (required for ``django-admin-index``)
* Add ``two_factor.plugins.webauthn`` to ``INSTALLED_APPS`` (required for ``maykin_2fa``)

0.4.0 (2024-06-06)
------------------

**New features**

* Add django-setup-configuration to deps
* Add ELASTIC_APM_TRANSACTION_SAMPLE_RATE

0.3.0 (2024-05-17)
------------------

**New features**

* [#14] Add django-log-outgoing-requests to deps
* [open-zaak/open-zaak#1629] Add generic base settings file


0.2.0 (2024-03-22)
------------------

**New features**

* Add support for python 3.10
* Upgrade to Django 4.2
* Add maykin-2fa


0.1.0 (2024-01-30)
------------------

* Initial release as a metapackage to pin several dependencies
