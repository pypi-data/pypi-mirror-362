from django.conf import settings
from django.urls import reverse

from django_webtest import WebTest


def test_sentry_settings():
    """
    test that sentry settings are initialized
    """

    assert hasattr(settings, "SENTRY_CONFIG") is True
    assert hasattr(settings, "SENTRY_DSN") is True


class RosettaTests(WebTest):
    def test_rosetta_redirect_fails_with_lazy_login_url(self):
        response = self.app.get("/admin/rosetta/files/project/")

        expected_login_url = (
            reverse(settings.LOGIN_URL) + "?next=/admin/rosetta/files/project/"
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, expected_login_url)
