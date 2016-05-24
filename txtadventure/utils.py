#coding=utf-8
# from django.shortcuts import render
from txtadventure.models import Player, Maps, Tiles, Enemies, Items#, ItemTypes


# from txtadventure import world
# from txtadventure import actions
# from txtadventure.player import Player as PP
# world.load_tiles()

# import time
import random

# Create your views here.
from django.http import HttpResponse

def randomEnemy(level,x,y):
    level = random.randint(1,level)+(level/3)
    ret = {}
    default_enemy_type = 100
    name = 'RandomEnemy'
    desc = 'Randome Enemy'
    baseamount = 10*level
    hp = random.randint(basemount, baseamount*3)
    damage = random.randint(baseamount-(hp/3), baseamount)
    class_name = "{}_{}_{}_{}".format(name,default_enemy_type,hp,damage)
    enemy = None
    #try:
    #    enemy = Enemies.objects.get(class_name=class_name)
    #except Enemies.DoesNotExist:
    #    enemy = Enemies(name=name, desc=desc, hp=hp, damage=damage, level=level, class_name=class_name)
    #    enemy.save()
    ret['class_name'] = enemy.class_name
    ret['name'] = enemy.name
    ret['hp'] = enemy.hp
    ret['damage'] = enemy.damage
    ret['desc'] = enemy.desc
    ret['level'] = enemy.level
    return ret

def dict_enemy(enemy):
    ret = {}
    ret['class_name'] = enemy.class_name
    ret['name'] = enemy.name
    ret['hp'] = enemy.hp
    ret['damage'] = enemy.damage
    ret['desc'] = enemy.desc
    ret['level'] = enemy.level
    return ret

def randomBlood(level):
    level = random.randint(1,level)
    ret = {}
    hp = level
    #hp = random.randint(1,level)
    ret['hp'] = hp
    ret['plus'] = random.randint(1,4)>1
    return ret

def randomItem(level):
    level = random.randint(1,level)
    ret = {}
    item_type = 'weapon'
    name = 'RandomWeapon'
    desc = 'Random Weapon'
    baseamount = 10*level
    damage = random.randint(1,baseamount)
    accu = random.randint(baseamount-damage, baseamount)
    crt = 0
    mulatt = 0
    value = (damage * accu / level) + crt + mulatt
    extra_param = {'damage': damage, 'accu': accu, 'crt': crt, 'mulatt': mulatt}
    class_name = "{}_{}_{}_{}_{}_{}".format(item_type, name, extra_param['damage'], extra_param['accu'],extra_param['crt'],extra_param['mulatt'])
    item = None
    #try:
    #    item = Items.objects.get(class_name=class_name)
    #except Items.DoesNotExist:
    #    item = Items(name=name, desc=desc, value=value, class_name=class_name, item_type=item_type, extra_params=str(extra_param))
    #    item.save()
    ret['class_name'] = item.class_name
    ret['damage'] = damage
    ret['accu'] = accu
    
    ret['amount'] = 1
    ret['item_type'] = item.item_type
    ret['name'] = item.name
    ret['value'] = item.value
    ret['desc'] = item.desc
    ret['level'] = item.level
    return ret

def randomRoad(inmap, x, y, way):
    t = None
    try:
        t = Tiles.objects.get(inmap=inmap, x=x, y=y)
    except Tiles.DoesNotExist:
        t = None
    if t:
        return getattr(t, way)
    else:
        return random.randint(1,4) > 1

def getTile(p):
    inmap = p.p.inmap
    x = p.location_x
    y = p.location_y
    level = p.level
    print x
    print y
    ret = None
    try:
        ret = Tiles.objects.get(inmap=inmap, x=x, y=y)
    except Tiles.DoesNotExist:
        ret = None
    
    if not ret:
        print '创建tile'
        n = randomRoad(inmap=inmap, x=x, y=y-1, way='s')
        s = randomRoad(inmap=inmap, x=x, y=y+1, way='n')
        e = randomRoad(inmap=inmap, x=x+1, y=y, way='w')
        w = randomRoad(inmap=inmap, x=x-1, y=y, way='e')
        
        #if n:
        #    pass
        #elif s:
        #    pass
        #elif w:
        #    pass
        #elif e:
        #    pass
        #else:
        #    e = True
            
        
        ret = Tiles(inmap=inmap, x=x, y=y, n=n, s=s, e=e, w=w)
        accy = {}
        if random.randint(1,3) > 1:
            accy['enemy'] = randomEnemy(level,x,y)
        if random.randint(1,2) == 1:
            accy['item'] = randomItem(level)
        if random.randint(1,4) == 1:
            accy['blood'] = randomBlood(level)
        ret.accy = str(accy)
        ret.save()
    else:
        if p.dienum>0 and p.souls>0:
            accy = eval(ret.accy)
            if 'enemy' in accy and accy['enemy']['hp'] <=0 and random.randint(1,5) == 1:
                try:
                    enemy = Enemies.objects.get(class_name=accy['enemy']['class_name'])
                    accy['enemy'] = dict_enemy(enemy)
                    p.souls -= 1
                except Enemies.DoesNotExist:
                    pass
                
            if 'item' in accy and accy['item']['amount']==0 and random.randint(1,5) == 1:
                accy['item'] = randomItem(level)
                
            ret.accy = str(accy)
            ret.save()
            # p.save()
    return ret
    

def levelup_info(pp):
    ret = '\n==恭喜！升级了！！==\n当前级别：{}.\n当前HP：{}\n'.format(pp.level,pp.hp)
    return ret

def die_info(pp):
    ret = '\n==挂了……==\n损失了一半经验T_T'
    return ret

def map_info(pp, resContent):
    inmap = pp.p.inmap
    print '地图信息：'
    print inmap.name
    print '：地图信息'
    x = pp.location_x
    y = pp.location_y
    showx ='0'
    showy ='0'
    if x > 0:
        showx ='东'+str(x)
        pass
    elif x < 0:
        showx ='西'+str(0-x)
        pass
    if y>0:
        showy ='南'+str(y)
        pass
    elif y<0:
        showy ='北'+str(0-y)
    tile = pp.tile
    accy  = eval(tile.accy)
    if 'enemy' in accy and accy['enemy']['hp']>=0:
        enemy_desc = "{}, 等级:{}, HP:{}, 攻击力:{}".format(accy['enemy']['name'], accy['enemy']['level'], accy['enemy']['hp'], accy['enemy']['damage'])
    else:
        enemy_desc = "【无】"
    
    if 'item' in accy and accy['item']['amount']:
        item_desc = "{}, 价值:{}, 攻击力:{}， 命中率:{}".format(accy['item']['name'], accy['item']['value'], accy['item']['damage'], accy['item']['accu'])
    else:
        item_desc = "【无】"
        
    tiledesc = "\n--------------\n=={}({},{})==:\n{}\n\n==遭遇敌人==:\n{}\n==发现物品==:\n{}\n".format(inmap.name, showx, showy, tile.desc, enemy_desc, item_desc)
    resContent += tiledesc
    return resContent
    
def actions_info(pp, resContent):
    resContent += '\n--------------\n==可选操作==:\n'
    inmap = pp.p.inmap
    x = pp.location_x
    y = pp.location_y
    tile = pp.tile
    acts = getAvailable_actions(tile,pp)
    for action in acts:
        resContent += str(action)
        resContent += '\n'
    return resContent
    
def adjacent_moves(tile):
    from txtadventure import actions
    acts = []
    if tile.e:
        acts.append(actions.MoveEast())
    if tile.w:
        acts.append(actions.MoveWest())
    if tile.n:
        acts.append(actions.MoveNorth())
    if tile.s:
        acts.append(actions.MoveSouth())
    return acts

def getAvailable_actions(tile, pp):
    from txtadventure import actions
    # ret = "\n--------------\n==可选操作==:\n"
    acts = []
    if pp.is_alive():
        accy = eval(tile.accy)
        if 'enemy' in accy and 'hp' in accy['enemy'] and accy['enemy']['hp']>0:
            acts.append(actions.Flee(tile))
            acts.append(actions.Attack(accy['enemy']))
        # else:
        #     if tile.e:
        #         acts.append(actions.MoveEast())
        #     if tile.w:
        #         acts.append(actions.MoveWest())
        #     if tile.n:
        #         acts.append(actions.MoveNorth())
        #     if tile.s:
        #         acts.append(actions.MoveSouth())
        
        if 'item' in accy and 'amount' in accy['item'] and accy['item']['amount']:
            acts.append(actions.Pick(accy['item']))
            pass
        
        if tile.e:
            acts.append(actions.MoveEast())
        if tile.w:
            acts.append(actions.MoveWest())
        if tile.n:
            acts.append(actions.MoveNorth())
        if tile.s:
            acts.append(actions.MoveSouth())
        
        
        acts.append(actions.ViewPlayerInfer())
        acts.append(actions.ViewInventory())
        
        # #GOD
        # if pp.p.inmap.wxoid == pp.p.wxoid:
        #     acts.append(actions.EditMap())
        # pass
    else:
        acts.append(actions.TrustChun())
        pass
    
    
    return acts
    
def help_info(pp, resContent):
    inmap = pp.p.inmap
    x = pp.location_x
    y = pp.location_y
    tile = pp.tile
    #resContent = map_info(pp, resContent)
    resContent = actions_info(pp, resContent)
    resContent = map_info(pp, resContent)
    return resContent


def hotkey_info(pp, resContent, receiveContent):
    inmap = pp.p.inmap
    x = pp.location_x
    y = pp.location_y
    tile = pp.tile
    acts = getAvailable_actions(tile,pp)
    
    # available_actions = room.available_actions()
    right_key = False
    for action in acts:
        
        if receiveContent.lower() == action.hotkey:
            print '输入：'
            print action.hotkey
            
            resContent += pp.do_action(action, **action.kwargs)
            right_key = True
            break
    
    pp.save()
    print '操作结果：'
    print resContent
    if right_key:
        return resContent
    else:
        return help_info(pp, resContent)
