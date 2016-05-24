#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import items, world
# import json
# import ast
from utils import help_info, map_info, getTile, adjacent_moves, die_info, levelup_info

from txtadventure.models import Items

class Player():
    def __init__(self, p):
        # self.inventory = [items.Gold(15), items.Rock()]
        self.name = p.name
        self.level = p.level
        self.souls = p.souls
        self.exp = p.exp
        self.dienum = p.dienum
        self.last_action = p.last_action
        # self.inventory = self.dic_inventory(p.inventory)
        self.inventory = eval(p.inventory)
        self.hp = p.hp
        self.location_x = p.location_x
        self.location_y = p.location_y
        self.victory = p.victory
        self.status = p.status
        self.money = p.money
        self.p = p
        
        self.tile = getTile(self)

    def save(self):
        self.p.hp = self.hp
        self.p.souls = self.souls
        self.p.last_action = self.last_action
        self.p.dienum = self.dienum
        self.p.exp = self.exp
        self.p.name = self.name
        self.p.level = self.level
        self.p.location_x = self.location_x
        self.p.location_y = self.location_y
        self.p.victory = self.victory
        self.p.status = self.status
        self.p.money = self.money
        # self.p.inventory = self.str_inventory(self.inventory)
        self.p.inventory = str(self.inventory)
        self.p.save()
    
    # def str_inventory(self, dic_inv):
    #     #sample: dic_inv
    #     #{1: {'item_type':'weapon', 'item': items.Rock()}, 2:{...}}
    #     ret = ""
    #     ret_dic = {}
    #     for k in dic_inv.keys():
    #         v = dic_inv[k]
    #         if v['item_type'] == 'weapon':
    #             ret_dic[k] = {'item_type':'weapon', 'item_class': v['item'].class_name}
    #     ret = str(ret_dic)
    #     print ret
    #     return ret
        
    # def dic_inventory(self, str_inv):
    #     #sample: str_inv
    #     #{1: {'item_type':'weapon', 'item_class': 'Rock'}, 2:{...}}
    #     ret = {}
    #     dic_inv = eval(str_inv)
    #     for k in dic_inv.keys():
    #         v = dic_inv[k]
    #         if v['item_type'] == 'weapon':
    #             # try:
    #             #     item = Items.objects.get(class_name=accy['item'])
    #             # except Items.DoesNotExist:
    #             #     item = None
    #             item = None if v['item_class'] == '' else getattr(items, v['item_class'])()
    #             ret[k] = {'item_type': 'weapon', 'item': item}
    #     print ret
    #     return ret
        
    def is_alive(self):
        return self.hp > 0

    def do_action(self, action, **kwargs):
        print 'action方法：'
        action_method = getattr(self, action.method.__name__)
        print action.method.__name__
        if action_method:
            res = action_method(**kwargs)
            return res
        else:
            return ''


    def add_items(self, item):
        nk = 0
        for k in self.inventory.keys():
            if k > nk:
                nk = k
        nk += 1
        self.inventory[nk] = {'item_type': item.item_type, 'item': item}
        pass
    
    def print_inventory(self):
        res = '==背包==:\n'
        for k in self.inventory.keys():
            item = self.inventory[k]
            res += "{}, 价值:{}, 攻击力:{}， 命中率:{}\n".format(item['name'], item['value'], item['damage'], item['accu'])
            v = self.inventory[k]
            # item = v['item']
            # res += str(item)
            # res += '\n'
            # print(item, '\n')
        # res += '<<背包'
        res += '\n'
        return res

    def print_player_info(self):
        res = '\n【{}】:\n'.format(self.name)
        res += '级别:{}\n'.format(self.level)
        res += '经验值：{}/{}'.format(self.exp, self.level*100)
        res += '生命值:{}\n'.format(self.hp)
        res += '地图:{}\n'.format(self.p.inmap.name)
        res += '坐标:[{},{}]\n'.format(self.location_x, self.location_y)
        res += '灵魂数：{}\n'.format(self.souls)
        res += '阵亡次数：{}\n'.format(self.dienum)
        res += '\n'
        return res

    def trust_chun(self):
        res = ''
        if self.hp > 0:
            res = '你还活着啊……算了，顺便把你送回家吧\n'
        else:
            res = '复活~！\n'
        self.location_x = 0
        self.location_y = 0
        self.hp = 100*self.level
        self.save()
        return res
        
    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        # self.p.location_x = self.location_x
        # self.p.location_y = self.location_y
        
        self.tile = getTile(self)
        ret = ""
        accy = eval(self.tile.accy)
        if 'blood' in accy:
            if accy['blood']['plus']:
                self.hp += accy['blood']['hp']*10
                if self.hp > 100 * self.level:
                    self.hp = 100 * self.level
                ret += '\n此地聚集正能量，恢复HP：{}点.\n'.format(accy['blood']['hp'])
            else:
                self.hp -= accy['blood']['hp']
                ret += '\n此地遇到负能量，减少HP：{}点.\n'.format(accy['blood']['hp'])
                if self.hp <=0:
                    ret += die_info(self)
                
            return ret
        return help_info(self, ret)
        #从tile.accy里判断item/enemy.desc来展示
        #item.exist
        #enemy.hp
        
        
        # print(world.tile_exists(self.location_x, self.location_y).intro_text())
        # room = world.tile_exists(self.location_x, self.location_y)
        # res = '[环境]：\n'
        # res += room.intro_text() or '[无]'
        # res += '\n\n'
        
        # return res

    def move_north(self):
        return self.move(dx=0, dy=-1)

    def move_south(self):
        return self.move(dx=0, dy=1)

    def move_east(self):
        return self.move(dx=1, dy=0)

    def move_west(self):
        return self.move(dx=-1, dy=0)

    def attack(self, enemy):
        # 
        #enemy might be None
        # 
        print '攻击：'
        best_weapon = None
        max_dmg = 0
        res = ''
        for k in self.inventory.keys():
            item = self.inventory[k]
            if not item['item_type'] == 'weapon':
                continue
            if item['damage'] > max_dmg:
                max_dmg = item['damage']
                best_weapon = item
            
            # v = self.inventory[k]
            # if v['item_type'] == 'weapon':
            #     if v['item'].damage > max_dmg:
            #         max_dmg = v['item'].damage
            #         best_weapon = v['item']
        
        if not best_weapon:
            res += '你没有武器……'
            return res
        res += "你用 {}(攻击{}，命中{}) 攻击 {}(Lv.{})!".format(best_weapon['name'], best_weapon['damage'], best_weapon['accu'], enemy['name'], enemy['level'])
        res += '\n'
        accu = best_weapon['accu']
        baseamount = 10 * enemy['level']
        if random.randint(1,baseamount) < accu:
            enemy['hp'] -= best_weapon['damage']
        else:
            res += "\n……没打中？！\n"
        accy = eval(self.tile.accy)
        accy['enemy'] = enemy
        # if 'enemy' in accy:
        #     accy['enemy']['hp'] = 0
        self.tile.accy = str(accy)
        self.tile.save()
        
        
        if enemy['hp']<=0:
            res += "你杀死了 {}!".format(enemy['name'])
            res += '\n'
            self.souls += 1
            getexp = (enemy['damage'])*enemy['level']/self.level
            #getexp = enemy['level']+ random.randint(20+5*enemy['level'],20+10*enemy['level'])
            self.exp += getexp
            res += '\n获得经验值：{}\n'.format(getexp)
            if self.exp > 100 * self.level:
                self.exp -= 100 * self.level
                self.level += 1
                self.hp = 100 * self.level
                
                res += levelup_info(self)
            # print("You killed {}!".format(enemy.name))
        else:
            res += "{} HP 剩余 {}.\n".format(enemy['name'], enemy['hp'])
            
            self.hp = self.hp - enemy['damage']
            res += "敌人造成 {} 点伤害. 你还剩 {} HP 的血量.\n".format(enemy['damage'], self.hp)
            if self.hp <= 0:
                self.exp /= 2
                self.dienum += 1
                res += die_info(self)
        
        return res
        
    
    def pickup(self, item):
        #modify player
        #modify tile
        print '拾取:'
        # nk = 0
        # for k in self.inventory.keys():
        #     if k > nk:
        #         nk = k
        # nk += 1
        # self.inventory[nk] = item
        # print item
        # accy = eval(self.tile.accy)
        # if 'item' in accy:
        #     accy['item']['amount'] = 0
        # self.tile.accy = str(accy)
        # self.tile.save()
        
        
        accy = eval(self.tile.accy)
        nk = 0
        picked = False
        for k in self.inventory.keys():
            if k>nk:
                nk = k+1
            if self.inventory[k]['item_type'] == 'weapon':
                #有装备，替换，包里只有一把武器
                if 'item' in accy:
                    accy['item'] = self.inventory[k]
                    
                self.inventory[k] = item
                picked = True
                break
        if not picked:
            #没有装备，拾取
            self.inventory[nk] = item
            if 'item' in accy:
                accy['item']['amount'] = 0
            
        self.tile.accy = str(accy)
        self.tile.save()
        return "获得物品：{}, 价值:{}, 攻击力:{}， 命中率:{}".format(item['name'], item['value'], item['damage'], item['accu'])
    
    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = adjacent_moves(tile)
        r = random.randint(0, len(available_moves) - 1)
        action = available_moves[r]
        return self.do_action(action, **action.kwargs)

