import os

import django
import pytest
from django.test import Client


from home.tests.tests import faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') #bez tego nie działa
django.setup()

from home.models import Feed

@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def set_up():
    for _ in range(5):
        Feed.objects.create(name=faker.name(),
                            notes=faker.paragraph(nb_sentences=3),
                            ingredients=faker.paragraph(nb_sentences=3))