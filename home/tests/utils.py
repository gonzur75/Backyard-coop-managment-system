import datetime
import random

from faker import Faker

from home.models import Feed, Flock, Weather

faker = Faker("pl_PL")


def feed_object():
    return Feed.objects.first()


def flock_object():
    return Flock.objects.first()


def get_weather_object():
    return Weather.objects.create(description=faker.name(), av_temp=random.randint(1, 25))

def fake_flock_data():
    fake_data = {
        "name": faker.name(),
        'notes': faker.paragraph(nb_sentences=2),
        'breed': faker.name(),
        'birds_count': random.randint(1, 40),
        'location': faker.city()
    }
    return fake_data

def fake_record_data():
    fake_data = {'date': faker.date(),
                 'collected_eggs': random.randint(1, 30),
                 'notes': faker.paragraph(nb_sentences=2),
                 'flock': flock_object(),
                 'weather': get_weather_object(),
                 'feed': feed_object(),
                 'feed_amount_kg': random.randint(1, 3)}
    return fake_data


