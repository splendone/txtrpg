from django.db import models

class Taxi(models.Model):
    location = models.IntegerField(max_length=10)
    timeField = models.IntegerField(max_length=10)
    peoples = models.IntegerField(max_length=10)
    taxies = models.IntegerField(max_length=10)
    pass
