{% load doc_tags %}.. _installation_env_config:

===================================
Environment configuration reference
===================================

{% block intro %}{% endblock %}

Available environment variables
===============================

{% for group_name, vars in vars %}
{{group_name}}
{{group_name|repeat_char:"-"}}

{% for var in vars %}* ``{{var.name}}``: {% if var.help_text %}{{var.help_text|safe|ensure_endswith:"."}}{% endif %}{% if var.auto_display_default and not var.default|is_undefined %} Defaults to: ``{{var.default|to_str|safe}}``.{% endif %}
{% endfor %}
{% endfor %}

{% block extra %}{% endblock %}

Specifying the environment variables
=====================================

There are two strategies to specify the environment variables:

* provide them in a ``.env`` file
* start the component processes (with uwsgi/gunicorn/celery) in a process
  manager that defines the environment variables

Providing a .env file
---------------------

This is the most simple setup and easiest to debug. The ``.env`` file must be
at the root of the project - i.e. on the same level as the ``src`` directory (
NOT *in* the ``src`` directory).

The syntax is key-value:

.. code::

   SOME_VAR=some_value
   OTHER_VAR="quoted_value"


Provide the envvars via the process manager
-------------------------------------------

If you use a process manager (such as supervisor/systemd), use their techniques
to define the envvars. The component will pick them up out of the box.
