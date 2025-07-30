from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("open_api_framework/components/version.html")
def version() -> dict:
    return {
        "version": getattr(settings, "RELEASE", ""),
        "git_sha": getattr(settings, "GIT_SHA", ""),
    }


@register.inclusion_tag("open_api_framework/components/environment.html")
def environment() -> dict:
    return {
        "environment": getattr(settings, "ENVIRONMENT", ""),
    }
