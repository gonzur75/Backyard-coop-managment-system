import os.path

import django
import pytest
from django.urls import reverse, reverse_lazy
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from home.models import Feed

faker = Faker("pl_PL")


@pytest.mark.django_db
def test_feed_view_get_request(client, set_up):
    response = client.get(reverse_lazy('home:feed'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_feed(client, set_up):

    feed_to_update = Feed.objects.first()
    new_name = faker.name()
    new_ingredients = faker.paragraph(nb_sentences=2)
    response = client.post(reverse('home:feed-update', kwargs={'pk': feed_to_update.id}),
                           {'name': new_name, 'ingredients': new_ingredients, 'notes': feed_to_update.notes})
    assert response.status_code == 302
    feed_object = Feed .objects.get(id=feed_to_update.id)
    assert feed_object.name == new_name
    assert feed_object.ingredients == new_ingredients


@pytest.mark.django_db
def test_delete_feed_get_request(client, set_up):
    """test whether feed confirm delete template is displayed"""
    feed_to_delete = Feed.objects.first()
    response = client.get(reverse('home:feed-delete', kwargs={'pk': feed_to_delete.id}), follow=True)
    delete_txt = f"delete {feed_to_delete.name}"
    assert delete_txt in str(response.content)


@pytest.mark.django_db
def test_delete_feed_post_request(client, set_up):
    """ test weather object is deleted """
    feed_to_delete = Feed.objects.first()
    response = client.post(reverse('home:feed-delete', kwargs={'pk': feed_to_delete.id}), follow=True)
    assert response.status_code == 200
    assert feed_to_delete not in Feed.objects.all()
