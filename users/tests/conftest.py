import os

import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # bez tego nie działa
django.setup()


@pytest.fixture(scope='function')
def user(db, django_user_model):
    user = django_user_model.objects.create_user(
        username="TestUser",
        email="test@test.com",
        password='TestPass123'
    )
    yield user


@pytest.fixture(scope='function')
def login(user, client):
    client.login(username='TestUser', password='TestPass123')
