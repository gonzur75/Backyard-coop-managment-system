import random

import pytest
from django.urls import reverse, reverse_lazy
from faker import Faker

from home.models import Flock
from home.tests.utils import feed_object, flock_object


faker = Faker("pl_PL")


@pytest.mark.django_db
def test_flock_view_get_request(client, login):
    response = client.get(reverse_lazy('home:flocks'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_flock(client, login):
    name = faker.name()
    ingredients = faker.paragraph(nb_sentences=2)
    notes = faker.paragraph(nb_sentences=2)
    response = client.post('/flocks/create/',
                           {'name': name,
                            'birds_count': random.randint(1, 30),
                            'notes': notes,
                            'breed': 'rosa',
                            'location': 'Bochnia'})

    assert Flock.objects.last().name == name
    assert response.status_code == 302





@pytest.mark.django_db
def test_update_flock(client, set_up, login):
    flock_test = flock_object()
    new_name = faker.name()
    new_notes = faker.paragraph(nb_sentences=2)
    response = client.post(reverse('home:flock-update', kwargs={'pk': flock_test.id}),
                           {'name': new_name,
                            'notes': new_notes,
                            'birds_count': flock_test.birds_count,
                            'breed': flock_test.breed,
                            'location': flock_test.location})
    assert response.status_code == 302
    test_object = Flock.objects.get(id=flock_test.id)
    assert test_object.name == new_name
    assert test_object.notes == new_notes


@pytest.mark.django_db
def test_delete_flock_get_request(client, set_up, login):
    """test whether flock confirm delete template is displayed"""
    flock_to_delete = Flock.objects.first()
    response = client.get(reverse('home:flock-delete', kwargs={'pk': flock_to_delete.id}), follow=True)
    delete_txt = f"delete {flock_to_delete.name}"
    assert delete_txt in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_delete_flock_post_request(client, set_up, login):
    """ test weather object is deleted """
    flock_to_delete = flock_object()
    response = client.post(reverse('home:flock-delete', kwargs={'pk': flock_to_delete.id}), follow=True)
    assert response.status_code == 200
    assert flock_to_delete not in Flock.objects.all()
