from home.models import Feed


def feed_object():
    return Feed.objects.first()