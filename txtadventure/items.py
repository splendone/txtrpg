#coding=utf-8
"""Describes the items in the game."""
__author__ = 'Phillip Johnson'


class Item(object):
    """The base class for all items"""
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return "{}：\n{}\n价值: {}\n".format(self.name, self.description, self.value)


class Weapon(Item):
    def __init__(self, name, description, value, item_type, damage):
        self.damage = damage
        self.item_type = item_type
        super(Weapon,self).__init__(name, description, value)

    def __str__(self):
        return "{}：\n{}\n价值: {}\n伤害值: {}".format(self.name, self.description, self.value, self.damage)


class Rock(Weapon):
    def __init__(self):
        self.class_name="Rock"
        super(Rock,self).__init__(name="石头",
                         description="一个拳头大小的石头.",
                         value=0,
                         item_type='weapon',
                         damage=5)


class Dagger(Weapon):
    def __init__(self):
        self.class_name="Dagger"
        super(Dagger,self).__init__(name="匕首",
                         description="一把生锈的小匕首. 攻击比石头高一些.",
                         value=10,
                         item_type='weapon',
                         damage=10)


class Gold(Item):
    def __init__(self, amt):
        self.amt = amt
        super(Gold, self).__init__(name="Gold",
                        description="A round coin with {} stamped on the front.".format(str(self.amt)),
                        value=self.amt)
