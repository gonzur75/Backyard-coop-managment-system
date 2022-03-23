import os
import random

import django
import pytest
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # bez tego nie działa
django.setup()

from home.tests.test_feed import faker
from home.tests.utils import fake_record_data, get_weather_object, fake_flock_data
from home.models import Feed, Flock, CoupeDay, Weather


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def set_up():
    for _ in range(3):
        get_weather_object()

    for _ in range(5):
        Feed.objects.create(name=faker.name(),
                            notes=faker.paragraph(nb_sentences=3),
                            ingredients=faker.paragraph(nb_sentences=3))
    for _ in range(2):
        Flock.objects.create(**fake_flock_data())
    for _ in range(5):
        CoupeDay.objects.create(**fake_record_data())

