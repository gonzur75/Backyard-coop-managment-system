import os

import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # bez tego nie działa
django.setup()
TEST_USERNAME = "TestUser"
TEST_EMAIL = "test@test.com"
TEST_PASSWORD = 'TestPass123'


@pytest.fixture(scope='function')
def user(db, django_user_model):
    user = django_user_model.objects.create_user(
        username=TEST_USERNAME,
        email=TEST_EMAIL,
        password=TEST_PASSWORD,
    )
    yield user


@pytest.fixture(scope='function')
def login(user, client):
    client.login(username='TestUser', password='TestPass123')
