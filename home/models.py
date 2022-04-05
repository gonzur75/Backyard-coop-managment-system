from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Flock(models.Model):
    # Flock holds data about flock
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    birds_count = models.IntegerField(verbose_name='birds')
    breed = models.CharField(max_length=64)
    notes = models.CharField(max_length=255)
    location = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:flocks')


class Feed(models.Model):
    # feed holds records of
    # difreent kind of feeds
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    ingredients = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:feed')


class Weather(models.Model):
    # weather will keep weather data on record day

    av_temp = models.SmallIntegerField()
    description = models.CharField(max_length=64)


class CoupeDay(models.Model):
    # record of one day in coupe
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField(unique=True, default=date.today)
    collected_eggs = models.IntegerField()
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    notes = models.CharField(max_length=255)
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    feed_amount_kg = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return f"record from {date}"

    def get_absolute_url(self):
        return reverse('home:records')
