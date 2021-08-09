from django.db import models

# Create your models here.
class RushingStatistic(models.Model):
    player = models.CharField(max_length=100)
    team = models.CharField(max_length=5)
    pos = models.CharField(max_length=5)
    att = models.IntegerField()
    att_g = models.FloatField()
    yds = models.IntegerField()
    avg = models.FloatField()
    yds_g = models.FloatField()
    td = models.IntegerField()
    lng = models.IntegerField()
    first = models.IntegerField()
    first_percentage = models.FloatField()
    twenty_plus = models.IntegerField()
    forty_plus = models.IntegerField()
    fum = models.IntegerField()