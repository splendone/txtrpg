#coding=utf-8
"""Defines the enemies in the game"""
__author__ = 'Phillip Johnson'


class Enemy(object):
    """A base class for all enemies"""
    def __init__(self, name, hp, damage):
        """Creates a new enemy

        :param name: the name of the enemy
        :param hp: the hit points of the enemy
        :param damage: the damage the enemy does with each attack
        """
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0


class GiantSpider(Enemy):
    def __init__(self):
        super(GiantSpider,self).__init__(name="巨大的蜘蛛", hp=10, damage=2)


class Ogre(Enemy):
    def __init__(self):
        super(Ogre,self).__init__(name="兽人", hp=30, damage=15)
