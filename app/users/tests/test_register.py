import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from users.tests.conftest import TEST_PASSWORD, TEST_EMAIL, TEST_USERNAME


@pytest.mark.django_db
def test_user_registration(client):
    response = client.post('/register/', {'username': TEST_USERNAME,
                                          'email': TEST_EMAIL,
                                          'password1': TEST_PASSWORD,
                                          'password2': TEST_PASSWORD,
                                          })
    assert response.status_code == 302
    user = get_user_model()
    assert user.objects.count() == 2

