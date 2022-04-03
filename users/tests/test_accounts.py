import os

import django
import pytest
from django.utils.http import int_to_base36

from users.tests.utils import USER_OLD_PASSWORD, USER_NEW_PASSWORD, utils_extract_uid_and_store_token_in_session

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # bez tego nie działa
django.setup()

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core import mail


def test_landing_page(client):
    """Checks if landing page is loading"""
    response = client.get(reverse('landing'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_change_password(client, user, login):
    """Checks if password is being changed"""
    response = client.post("/accounts/password_change/", {'old_password': USER_OLD_PASSWORD,
                                                          'new_password1': USER_NEW_PASSWORD,
                                                          'new_password2': USER_NEW_PASSWORD, })
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.check_password(USER_NEW_PASSWORD) is True


@pytest.mark.django_db
def test_change_password_done_message(client, user, login):
    """Checks weather password_change_done.html template is being displayed"""

    response = client.post("/accounts/password_change/", {'old_password': USER_OLD_PASSWORD,
                                                          'new_password1': USER_NEW_PASSWORD,
                                                          'new_password2': USER_NEW_PASSWORD, }, follow=True)
    assert 'Password changed' in response.content.decode('UTF-8')
    assert response.status_code == 200


@pytest.mark.django_db
def test_reset_password_initial_form(client):
    """Checks weather password_reset_form.html template is being displayed"""

    response = client.post('/accounts/password_reset/')
    assert response.status_code == 200
    assert 'registration/password_reset_form.html' in response.template_name


def test_reset_password_response(client, user):
    """Checks weather reset password email is being sent"""
    response = client.post(reverse('password_reset'), {'email': user.email})
    assert response.status_code == 302
    assert len(mail.outbox) == 1


def test_reset_password_change_form(client, user):
    """Checks weather password_reset_confirm.html is displayed after activating email link"""

    token = default_token_generator.make_token(user)
    uid = int_to_base36(user.id)
    response = client.get(reverse('password_reset_confirm', kwargs={'token': token,
                                                                    'uidb64': uid}))

    assert response.status_code == 200
    assert 'registration/password_reset_confirm.html' in response.template_name


def test_reset_password_change_done(client, user):
    """ Checks weather password is changed after new password is entered"""
    # Because django stores token in session to avoid it being leaked in 'HTTP Referer header',
    # we have to, first hit password reset with get so django can store token in session.

    uid = utils_extract_uid_and_store_token_in_session(client, user)

    # Then we use post to reset password, but with token as 'set-password'.
    response = client.post(reverse('password_reset_confirm', kwargs={'token': "set-password", 'uidb64': uid}),
                           {'new_password1': USER_NEW_PASSWORD, 'new_password2': USER_NEW_PASSWORD})

    assert response.status_code == 302.
    user.refresh_from_db()
    assert user.check_password(USER_NEW_PASSWORD) is True


def test_reset_password_complete(client, user):
    """Checks weather password_reset_complete.html template is displayed following successful password change"""
    uid = utils_extract_uid_and_store_token_in_session(client, user)
    response = client.post(reverse('password_reset_confirm', kwargs={'token': 'set-password', 'uidb64': uid}),
                           {'new_password1': USER_NEW_PASSWORD, 'new_password2': USER_NEW_PASSWORD}, follow=True)
    assert response.status_code == 200
    assert 'registration/password_reset_complete.html' in response.template_name


