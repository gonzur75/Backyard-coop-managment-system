from django.db import models


class Flock(models.Model):
    # Flock holds data about flock
    name = models.CharField(max_length=64)
    birds_count = models.IntegerField(verbose_name='birds')
    breed = models.CharField(max_length=64)
    notes = models.CharField(max_length=255)


class Feed(models.Model):
    # Feed holds records of difreent kind of feeds
    name = models.CharField(max_length=64)
    ingredients = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)


class Weather(models.Model):
    # weather will keep weather data on record day
    location = models.CharField(max_length=64)
    av_temp = models.SmallIntegerField()
    description = models.CharField(max_length=64)


class CoupeDay(models.Model):
    # record of one day in coupe
    date = models.DateField(unique=True)
    collected_eggs = models.IntegerField()
    flock = models.ForeignKey(Flock, on_delete=models.PROTECT)
    notes = models.CharField(max_length=255)
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.PROTECT)
    feed_amount_kg = models.DecimalField(max_digits=4, decimal_places=1)

