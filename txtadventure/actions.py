#coding=utf-8
"""Describes the actions a player can make in the game"""
__author__ = 'Phillip Johnson'

from player import Player


class Action(object):
    """The base class for all actions"""
    def __init__(self, method, name, hotkey, **kwargs):
        """Creates a new action

        :param method: the function object to execute
        :param name: the name of the action
        :param ends_turn: True if the player is expected to move after this action else False
        :param hotkey: The keyboard key the player should use to initiate this action
        """
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs

    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)


class MoveNorth(Action):
    def __init__(self):
        super(MoveNorth,self).__init__(method=Player.move_north, name='往北走', hotkey='n')


class MoveSouth(Action):
    def __init__(self):
        super(MoveSouth,self).__init__(method=Player.move_south, name='往南走', hotkey='s')


class MoveEast(Action):
    def __init__(self):
        super(MoveEast,self).__init__(method=Player.move_east, name='往东走', hotkey='e')


class MoveWest(Action):
    def __init__(self):
        super(MoveWest,self).__init__(method=Player.move_west, name='往西走', hotkey='w')


class ViewInventory(Action):
    """Prints the player's inventory"""
    def __init__(self):
        super(ViewInventory,self).__init__(method=Player.print_inventory, name='查看背包', hotkey='b')

class ViewPlayerInfer(Action):
    """Prints the player's inventory"""
    def __init__(self):
        super(ViewPlayerInfer,self).__init__(method=Player.print_player_info, name='玩家信息', hotkey='i')

class Attack(Action):
    def __init__(self, enemy):
        super(Attack,self).__init__(method=Player.attack, name="攻击", hotkey='a', enemy=enemy)


class Flee(Action):
    def __init__(self, tile):
        super(Flee,self).__init__(method=Player.flee, name="逃跑", hotkey='f', tile=tile)

class Pick(Action):
    def __init__(self, item):
        super(Pick,self).__init__(method=Player.pickup, name="拾取", hotkey='p', item=item)

class TrustChun(Action):
    def __init__(self):
        super(TrustChun,self).__init__(method=Player.trust_chun, name="信春哥", hotkey='r')
        
        
# class EditMap(Action):
#     """Prints the player's inventory"""
#     def __init__(self):
#         super(ViewInventory,self).__init__(method=Player.print_inventory, name='修改地图', hotkey='cm')
