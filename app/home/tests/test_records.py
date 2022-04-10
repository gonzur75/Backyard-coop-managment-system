import pytest
from django.urls import reverse, reverse_lazy

from home.models import Flock, CoupeDay
from home.tests.conftest import user
from home.tests.utils import feed_object, flock_object, fake_record_data, faker



@pytest.mark.django_db
def test_records_view_get_request(client, login):
    response = client.get(reverse_lazy('home:records'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_record(client, set_up, login):
    """test whether record is saved to database"""
    record_data = fake_record_data(user)
    record_data['flock'] = record_data['flock'].id
    record_data['feed'] = record_data['feed'].id
    response = client.post('/record/create/', data=record_data, follow=True)
    assert response.status_code == 200
    assert CoupeDay.objects.count() == 6


@pytest.mark.django_db
def test_update_record(client, set_up, login):
    """test whether record is updated in database"""
    record_test = CoupeDay.objects.first()
    new_notes = faker.paragraph(nb_sentences=2)
    response = client.post(reverse('home:record-update', kwargs={'pk': record_test.id}),
                           {
                            'date': record_test.date,
                            'notes': new_notes,
                            'collected_eggs': record_test.collected_eggs,
                            'flock': record_test.flock.pk,
                            'feed': record_test.feed.pk,
                            'feed_amount_kg': record_test.feed_amount_kg
                            })
    assert response.status_code == 302
    object_feed = CoupeDay.objects.get(id=record_test.id)
    assert object_feed.notes == new_notes


@pytest.mark.django_db
def test_delete_record_get_request(client, set_up, login):
    """test if record confirm delete template is displayed"""
    record_to_delete = CoupeDay.objects.first()
    response = client.get(reverse('home:record-delete', kwargs={'pk': record_to_delete.id}), follow=True)
    delete_txt = f"Confirm delete"
    assert delete_txt in response.content.decode('UTF-8')


@pytest.mark.django_db
def test_delete_record_post_request(client, set_up, login):
    """ test if object is deleted """
    record_to_delete = CoupeDay.objects.first()
    response = client.post(reverse('home:record-delete', kwargs={'pk': record_to_delete.id}), follow=True)
    assert response.status_code == 200
    assert record_to_delete not in Flock.objects.all()
