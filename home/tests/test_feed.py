import pytest
from django.urls import reverse, reverse_lazy
from faker import Faker

from home.models import Feed
from home.tests.utils import feed_object

faker = Faker("pl_PL")


@pytest.mark.django_db
def test_feed_view_get_request(client,login):
    response = client.get(reverse_lazy('home:feed'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_feed(client, login):
    name = faker.name()
    ingredients = faker.paragraph(nb_sentences=2)
    notes = faker.paragraph(nb_sentences=2)
    response = client.post('/feed/create/',{
                            'name': name,
                            'ingredients': ingredients,
                            'notes': notes})

    assert Feed.objects.last().name == name
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_feed(client, set_up, login):
    new_name = faker.name()
    new_ingredients = faker.paragraph(nb_sentences=2)
    response = client.post(reverse('home:feed-update', kwargs={'pk': feed_object().id}),
                           {'name': new_name, 'ingredients': new_ingredients, 'notes': feed_object().notes})
    assert response.status_code == 302
    object_feed = Feed.objects.get(id=feed_object().id)
    assert object_feed.name == new_name
    assert object_feed.ingredients == new_ingredients


@pytest.mark.django_db
def test_delete_feed_get_request(client, set_up, login):
    """test whether feed confirm delete template is displayed"""
    feed_to_delete = Feed.objects.first()
    response = client.get(reverse('home:feed-delete', kwargs={'pk': feed_object().id}), follow=True)
    delete_txt = f"delete {feed_object().name}"
    assert delete_txt in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_delete_feed_post_request(client, set_up, login):
    """ test weather object is deleted """
    feed_to_delete = feed_object()
    response = client.post(reverse('home:feed-delete', kwargs={'pk': feed_object().id}), follow=True)
    assert response.status_code == 200
    assert feed_to_delete not in Feed.objects.all()
