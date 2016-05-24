from django.db import models

# Create your models here.

class Maps(models.Model):
    name = models.CharField(max_length=100, default="DefaultMap")
    desc = models.TextField(default="default map description.")
    level = models.IntegerField(default=1)
    enter = models.TextField(default="{}")
    wxoid = models.TextField(default="")
    pass

class Player(models.Model):
    wxoid = models.TextField()
    name = models.CharField(max_length=100)
    money = models.IntegerField(default=33)
    hp = models.IntegerField(default=100)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=1)
    victory = models.BooleanField(default=False)
    status = models.IntegerField(default=0)
    inmap = models.ForeignKey(Maps)
    location_x = models.IntegerField(default=0)
    location_y = models.IntegerField(default=0)
    inventory = models.TextField(default="{}")#{1: {'item_type': 'weapon', 'item_class': 'Rock_2_2_100'}}
    souls = models.IntegerField(default=0)
    dienum = models.IntegerField(default=0)
    last_action = models.CharField(max_length=100, default='h')
    pass



class Tiles(models.Model):
    inmap = models.ForeignKey(Maps)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    accy = models.TextField(default="{}")
    n = models.BooleanField(default=False)
    s = models.BooleanField(default=False)
    e = models.BooleanField(default=False)
    w = models.BooleanField(default=False)
    desc = models.TextField(default="")
    pass
    
class Enemies(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    enemy_type = models.IntegerField(default=100)
    level = models.IntegerField(default=1)
    hp = models.IntegerField(default=10)
    damage = models.IntegerField(default=0)
    desc = models.TextField(default="default description.")

# class ItemTypes(models.Model):
#     name = models.CharField(max_length=100)
#     item_type = models.CharField(max_length=100)
#     class_name = models.CharField(max_length=100)
#     extra_params = models.TextField(default="{}")
    
class Items(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(default=0)
    class_name = models.CharField(max_length=100)
    desc = models.TextField(default="default description.")
    item_type = models.CharField(max_length=100)
    extra_params = models.TextField(default="{}")
    level = models.IntegerField(default=1)
