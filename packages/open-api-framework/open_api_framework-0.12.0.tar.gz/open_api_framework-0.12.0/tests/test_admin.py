from django.contrib.sessions.backends.cache import SessionStore as CachedSessionStore
from django.contrib.sessions.backends.db import SessionStore as DBSessionStore
from django.contrib.sessions.models import Session
from django.test import override_settings
from django.urls import reverse

import pytest
from sessionprofile.models import SessionProfile

from open_api_framework.utils import get_session_store

from .factories import SessionProfileFactory


@pytest.fixture
def session_changelist_url():
    return reverse("admin:sessionprofile_sessionprofile_changelist")


def test_session_profile_sanity(client, admin_user, session_changelist_url):
    client.force_login(admin_user)
    response = client.get(session_changelist_url)
    assert response.status_code == 200

    assert SessionProfile.objects.count() == 1

    session = SessionProfile.objects.get()
    assert client.session.session_key == session.session_key


def test_only_session_profile_of_user_shown(
    client, admin_user, django_user_model, session_changelist_url
):
    other_admin = django_user_model.objects.create_superuser("garry")

    client.force_login(other_admin)
    response = client.get(session_changelist_url)
    assert response.status_code == 200

    client.force_login(admin_user)
    response = client.get(session_changelist_url)
    assert response.status_code == 200

    # two sessions, one for each user
    assert SessionProfile.objects.count() == 2

    # Session created after response, needs to be called again
    response = client.get(session_changelist_url)

    admin_user_session = SessionProfile.objects.get(user=admin_user)
    assert admin_user_session.session_key in response.content.decode()

    other_user_session = SessionProfile.objects.get(user=other_admin)
    assert other_user_session.session_key not in response.content.decode()

    # should only be able to access own page
    change_url = reverse(
        "admin:sessionprofile_sessionprofile_change",
        args=[admin_user_session.session_key],
    )
    response = client.get(change_url)
    assert response.status_code == 200

    change_url = reverse(
        "admin:sessionprofile_sessionprofile_change",
        args=[other_user_session.session_key],
    )
    response = client.get(change_url)
    assert response.status_code == 302
    assert response.url == reverse("admin:index")


def test_cant_delete_other_users_session(client, admin_user, django_user_model):
    client.force_login(admin_user)

    other_admin = django_user_model.objects.create_superuser("garry")

    other_user_session = SessionProfileFactory(user=other_admin)

    delete_url = reverse(
        "admin:sessionprofile_sessionprofile_delete",
        args=[other_user_session.session_key],
    )

    response = client.post(delete_url, {"post": "yes"})
    assert response.status_code == 302

    SessionStore = get_session_store()

    assert SessionStore().exists(other_user_session.session_key)


def test_delete_with_session_db_backend(client, admin_user, session_changelist_url):
    client.force_login(admin_user)

    session = SessionProfileFactory(user=admin_user)

    assert SessionProfile.objects.count() == 1
    # sesison created by login
    assert Session.objects.count() == 2
    assert DBSessionStore().exists(session.session_key)

    url = reverse("admin:sessionprofile_sessionprofile_delete", args=[session.pk])

    response = client.post(url, {"post": "yes"})
    assert response.status_code == 302

    # new session saved upon request
    assert SessionProfile.objects.count() == 1
    assert SessionProfile.objects.count() != session
    assert Session.objects.count() == 1
    assert not DBSessionStore().exists(session.session_key)


@override_settings(SESSION_ENGINE="django.contrib.sessions.backends.cache")
def test_delete_with_session_cache_backend(client, admin_user, session_changelist_url):
    client.force_login(admin_user)

    session = SessionProfileFactory(user=admin_user)

    assert SessionProfile.objects.count() == 1
    assert Session.objects.count() == 0
    assert CachedSessionStore().exists(session.session_key)

    url = reverse("admin:sessionprofile_sessionprofile_delete", args=[session.pk])

    response = client.post(url, {"post": "yes"})
    assert response.status_code == 302

    # new session saved upon request
    assert SessionProfile.objects.count() == 1
    assert SessionProfile.objects.count() != session
    assert Session.objects.count() == 0
    assert not CachedSessionStore().exists(session.session_key)


def test_delete_action_with_session_db_backend(
    client, admin_user, session_changelist_url
):
    client.force_login(admin_user)
    sessions = SessionProfileFactory.create_batch(5, user=admin_user)

    # one created from user login
    assert Session.objects.count() == 6
    assert SessionProfile.objects.count() == 5

    session_keys = [session.session_key for session in sessions]
    for session_key in session_keys:
        assert DBSessionStore().exists(session_key)

    response = client.post(
        session_changelist_url,
        {"action": "delete_selected", "_selected_action": session_keys, "post": "yes"},
    )
    assert response.status_code == 302

    # one is created as the post request is sent
    assert SessionProfile.objects.count() == 1
    assert Session.objects.count() == 1

    for session_key in session_keys:
        assert not DBSessionStore().exists(session_key)


@override_settings(SESSION_ENGINE="django.contrib.sessions.backends.cache")
def test_delete_action_with_session_cache_backend(
    client, admin_user, session_changelist_url
):
    client.force_login(admin_user)
    sessions = SessionProfileFactory.create_batch(5, user=admin_user)

    # no db sessions are created
    assert Session.objects.count() == 0
    assert SessionProfile.objects.count() == 5

    session_keys = [session.session_key for session in sessions]

    # sessions are created
    for session_key in session_keys:
        assert CachedSessionStore().exists(session_key)

    response = client.post(
        session_changelist_url,
        {"action": "delete_selected", "_selected_action": session_keys, "post": "yes"},
    )
    assert response.status_code == 302

    # one is created as the post request is sent
    assert SessionProfile.objects.count() == 1
    assert Session.objects.count() == 0

    # sessions should be deleted
    for session_key in session_keys:
        assert not CachedSessionStore().exists(session_key)
