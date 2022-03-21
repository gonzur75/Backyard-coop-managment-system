import os
import random

import django
import pytest
from django.test import Client


from home.tests.tests_feed import faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') #bez tego nie działa
django.setup()

from home.models import Feed, Flock


@pytest.fixture
def client():
    client = Client()
    return client


def fake_flock_data():
    fake_data = {
        "name": faker.name(),
        'notes': faker.paragraph(nb_sentences=2),
        'breed': faker.name(),
        'birds_count': random.randint(1, 40),
        'location': faker.city()
    }
    return fake_data


@pytest.fixture
def set_up():
    for _ in range(5):
        Feed.objects.create(name=faker.name(),
                            notes=faker.paragraph(nb_sentences=3),
                            ingredients=faker.paragraph(nb_sentences=3))

    for _ in range(2):
        Flock.objects.create(**fake_flock_data())
