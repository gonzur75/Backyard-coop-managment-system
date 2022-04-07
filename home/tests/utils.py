import random

from faker import Faker

from home.models import Feed, Flock, Weather, Location

faker = Faker("pl_PL")


def feed_object():
    return Feed.objects.first()


def flock_object():
    return Flock.objects.first()


def get_weather_object():
    return Weather.objects.create(description=faker.name(), av_temp=random.randint(1, 25))


def get_location_object():
    location = Location.objects.create(
        name=faker.name(),
        # coordinates for Krakow
        lat=50.061389,
        lon=19.938333,
    )
    return location


def fake_flock_data(user):
    fake_data = {
        'author': user,
        'name': faker.name(),
        'notes': faker.paragraph(nb_sentences=2),
        'breed': faker.name(),
        'birds_count': random.randint(1, 40),
        'location': get_location_object()
    }
    return fake_data


def fake_record_data(user):
    fake_data = {
        'author': user,
        'date': faker.date(),
        'collected_eggs': random.randint(1, 30),
        'notes': faker.paragraph(nb_sentences=2),
        'flock': flock_object(),
        'weather': get_weather_object(),
        'feed': feed_object(),
        'feed_amount_kg': random.randint(1, 3)
    }
    return fake_data


def fake_feed_data(user):
    data = {
        'author': user,
        'name': faker.name(),
        'notes': faker.paragraph(nb_sentences=3),
        'ingredients': faker.paragraph(nb_sentences=3)
    }
    return data
