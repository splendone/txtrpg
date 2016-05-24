from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Battle(models.Model):
    wxoid = models.TextField()
    enflight = models.TextField(default='')
    myflight = models.TextField(default='')
    fires = models.TextField(default='{}')
    win = models.IntegerField(default=0)

class Pilot(models.Model):
    wxoid = models.TextField()
    status = models.IntegerField(default=0)
    battle = models.ForeignKey(Battle)
    best = models.IntegerField(default=999)


class Biaoqing(models.Model):
    name = models.CharField(max_length=10)
    unc = models.CharField(max_length=10)
    seq = models.IntegerField()
