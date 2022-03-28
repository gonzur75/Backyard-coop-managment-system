import os

import django
import pytest
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # bez tego nie działa
django.setup()

from home.tests.test_feed import faker
from home.tests.utils import fake_record_data, get_weather_object, fake_flock_data
from home.models import Feed, Flock, CoupeDay




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