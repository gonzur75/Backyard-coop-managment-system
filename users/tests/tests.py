import os

import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # bez tego nie działa
django.setup()

from django.urls import reverse, reverse_lazy
from django.core import mail



def test_landing_page(client):
    response = client.get(reverse('landing'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_change_password(client, user, login):
    response = client.post("/accounts/password_change/", {'old_password': 'TestPass123',
                                                          'new_password1': 'TestPass1234',
                                                          'new_password2': 'TestPass1234', })
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.check_password('TestPass1234') is True


@pytest.mark.django_db
def test_change_password_done_message(client, user, login):
    response = client.post("/accounts/password_change/", {'old_password': 'TestPass123',
                                                          'new_password1': 'TestPass1234',
                                                          'new_password2': 'TestPass1234', }, follow=True)
    assert 'Password changed' in response.content.decode('UTF-8')
    assert response.status_code == 200

@pytest.mark.django_db
def test_reset_password_initial_form(client):
    response = client.post('/accounts/password_reset/')
    assert response.status_code == 200
    assert 'registration/password_reset_form.html' in response.template_name


def test_reset_password_response(client, user):
    response = client.post(reverse('password_reset'), {'email': user.email})
    assert response.status_code == 302
    assert len(mail.outbox) == 1

def test_reset_password_change_form(client, user):
    response = client.post(reverse('password_reset'), {'email': user.email})
    token = response.context[0]['token']
    uid = response.context[0]['uid']

    response = client.get(reverse('password_reset_confirm', kwargs={'token': token,
                                                                    'uidb64': uid}))
    print(response)
    assert response.status_code == 302
    assert response.template_name == 'acounts/password_reset_confirm.html'