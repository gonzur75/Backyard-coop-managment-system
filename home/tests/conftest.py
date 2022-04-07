import os

import django
import pytest
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # bez tego nie działa
django.setup()

from home.tests.utils import fake_record_data, get_weather_object, fake_flock_data, fake_feed_data
from home.models import Feed, Flock, CoupeDay


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def set_up(user):
    for _ in range(3):
        get_weather_object()

    for _ in range(5):
        Feed.objects.create(**fake_feed_data(user))
    for _ in range(2):
        Flock.objects.create(**fake_flock_data(user))
    for _ in range(5):
        CoupeDay.objects.create(**fake_record_data(user))


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
