import os

import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # bez tego nie działa
django.setup()

from django.contrib.auth.models import User
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # bez tego nie działa
django.setup()


def test_landing_page(client):
    response = client.get(reverse('landing'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_reset_password(client, user, login):
    response = client.post("/accounts/password_change/", {'old_password': 'TestPass123',
                                                          'new_password1': 'TestPass1234',
                                                          'new_password2': 'TestPass1234', })
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.check_password('TestPass1234') is True


@pytest.mark.django_db
def test_reset_password_done_message(client, user, login):
    response = client.post("/accounts/password_change/", {'old_password': 'TestPass123',
                                                          'new_password1': 'TestPass1234',
                                                          'new_password2': 'TestPass1234', }, follow=True)
    assert 'Password changed' in response.content.decode('UTF-8')
    assert response.status_code == 200
