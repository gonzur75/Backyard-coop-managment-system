from django.urls import reverse

USER_OLD_PASSWORD = 'TestPass123'
USER_NEW_PASSWORD ='TestPass1234'


def utils_extract_uid_and_store_token_in_session(client, user):
    """
    Because django stores token in session to avoid it being leaked in 'HTTP Referer header',
    we have to, first hit password reset with get so django can store token in session.
    In process we can also extract user id wich we will use in test
    """

    response = client.post(reverse('password_reset'), {'email': user.email})
    uid = response.context[0]['uid']
    token = response.context[0]['token']
    client.get(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}), follow=True)
    return uid