#coding=utf-8
from django.shortcuts import render
from dafeiji.models import Biaoqing, Pilot, Battle

# Create your views here.

import random

BTSIZE = 6 

bq1 = Biaoqing.objects.get(seq = 68)#云
bq2 = Biaoqing.objects.get(seq = 66)#太阳
bq3 = Biaoqing.objects.get(seq = 45)#火
bq4 = Biaoqing.objects.get(seq = 64)#骷髅
bq5 = Biaoqing.objects.get(seq = 162)#男人
bq6 = Biaoqing.objects.get(seq = 163)#女人
bq7 = Biaoqing.objects.get(seq = 164)#o
bq8 = Biaoqing.objects.get(seq = 165)#x

warr = ['a', 's' , 'd', 'w']
xarr = ['/::)', '/::~', '/::B', '/::|', '/:8-)', '/::$']
yarr = ['/::X', '/::Z', '/::-|', '/::@', '/::P', '/::D']

strshape = {
    'a':[(1,0),(2,0),(3,0),(1,-1),(1,-2),(1,1),(1,2),(3,-1),(3,1)],
    's':[(0,-1),(0,-2),(0,-3),(-1,-1),(-2,-1),(1,-1),(2,-1),(-1,-3),(1,-3)],
    'd':[(-1,0),(-2,0),(-3,0),(-1,-1),(-1,-2),(-1,1),(-1,2),(-3,-1),(-3,1)],
    'w':[(0,1),(0,2),(0,3),(-1,1),(-2,1),(1,1),(2,1),(-1,3),(1,3)],
}
shape = [
    [(1,0),(2,0),(3,0),(1,-1),(1,-2),(1,1),(1,2),(3,-1),(3,1)],
    [(0,-1),(0,-2),(0,-3),(-1,-1),(-2,-1),(1,-1),(2,-1),(-1,-3),(1,-3)],
    [(-1,0),(-2,0),(-3,0),(-1,-1),(-1,-2),(-1,1),(-1,2),(-3,-1),(-3,1)],
    [(0,1),(0,2),(0,3),(-1,1),(-2,1),(1,1),(2,1),(-1,3),(1,3)],
]

def fj_line(w,x,y,l):
    #xarr = ['/::)', '/::~', '/::B', '/::|', '/:8-)', '/::$']
    print 'w:{}  x:{}  y:{}  l:{}'.format(w,x,y,l)
    arr = [bq1.unc]*BTSIZE

    if l == y:
        arr[x] = bq6.unc
    shapew = shape[w]
    for w in shapew:
        xx = x + w[0]
        yy = y + w[1]
        if l == yy:
            arr[xx] = bq5.unc
    return arr

def randomLocation():
    ranw = random.randint(0,3)
    ranx = 0
    rany = 0
    if ranw == 0:
        ranx = random.randint(0, BTSIZE-4)
        rany = random.randint(2, BTSIZE-3)
    if ranw == 1:
        ranx = random.randint(2, BTSIZE-3)
        rany = random.randint(3, BTSIZE-1)
    if ranw == 2:
        ranx = random.randint(3, BTSIZE-1)
        rany = random.randint(2, BTSIZE-3)
    if ranw == 3:
        ranx = random.randint(2, BTSIZE-3)
        rany = random.randint(0, BTSIZE-4)
    return (ranw,ranx,rany)

def showFeijiFire(ranw,ranx,rany, frs):
    showf = [bq2.unc]
    showf.extend(xarr)
    showf.append('\n')
    for i in range(BTSIZE):
        showf.append(yarr[i])

        fjl = fj_line(ranw,ranx,rany,i)
        arr = [bq1.unc]*BTSIZE
        if i in frs:
            for x in frs[i]:
                if fjl[x] == bq6.unc:#击落
                    arr[x] = bq4.unc
                elif fjl[x] == bq5.unc:#击中
                    arr[x] = bq3.unc
                elif fjl[x] == bq1.unc:#未击中
                    arr[x] = bq8.unc
            showf.extend(arr)
        else:
            showf.extend(arr)

        #showf.extend(fj_line(ranw,ranx,rany,i))
        showf.append('\n')
    return showf

def showFeiji(ranw,ranx,rany):
    showf = [bq2.unc]
    showf.extend(xarr)
    showf.append('\n')
    for i in range(BTSIZE):
        showf.append(yarr[i])
        showf.extend(fj_line(ranw,ranx,rany,i))
        showf.append('\n')
    return showf
    #return ''.join(showf)

def checkBiaoqing(rec):
    sp = rec.split('/')
    cbq = {'ok':False, 'xy':[0,0]}
    
    if len(sp) == 3:
        x = '/'+sp[1]
        y = '/'+sp[2]
        print 'bqx:{}, bqy:{}'.format(x,y)
        if x in xarr:
            cbq['xy'][0] = xarr.index(x)
        else:
            cbq['ok'] = False
            return cbq
        if y in yarr:
            cbq['xy'][1] = yarr.index(y)
        else:
            cbq['ok'] = False
            return cbq
        cbq['ok'] = True
    return cbq

def fire(pilot, xy):
    print xy
    frs = eval(pilot.battle.fires)
    print frs
    if xy[1] in frs:
        if xy[0] not in frs[xy[1]]:
            frs[xy[1]].append(xy[0])
    else:
        frs[xy[1]] = [xy[0]]
    pilot.battle.fires = str(frs)
    enflight = eval(pilot.battle.enflight)
    enw = enflight[0]
    enx = enflight[1]
    eny = enflight[2]
    if xy[0] == enx and xy[1] == eny:
        pilot.battle.win = 1
    pilot.battle.save()
    return ''.join(showFeijiFire(enw,enx,eny,frs))
    #return 'fire...'

def resultInfo(pilot):
    if pilot.battle.win == 1:
        ret = '\nYou Win!\n Enemy:\n'
        frs = eval(pilot.battle.fires)
        enflight = eval(pilot.battle.enflight)
        enw = enflight[0]
        enx = enflight[1]
        eny = enflight[2]
        ret += ''.join(showFeiji(enw,enx,eny))
        best = 0
        obest = pilot.best
        for k in frs:
            best += len(frs[k])
        if best < obest:
            pilot.best = best
            pilot.save()
            ret += '\nFire {} times. New Best!!!\n'.format(best)
        else:
            ret += '\nFire {} times. Your Best: {} times.\n'.format(best, obest)
        return ret
    else:
        return ''

def helpInfo(pilot):
    ret = '敌机形状如下，敌机位置和朝向未知，击中{}获胜：\n'.format(bq6.unc)
    myflight = eval(pilot.battle.myflight)
    myw = myflight[0]
    myx = myflight[1]
    myy = myflight[2]
    ret += ''.join(showFeiji(myw,myx,myy))
    ret += '\n敌机：\n'
    frs = eval(pilot.battle.fires)
    enflight = eval(pilot.battle.enflight)
    enw = enflight[0]
    enx = enflight[1]
    eny = enflight[2]
    ret += ''.join(showFeijiFire(enw,enx,eny,frs))
    ret += '\n攻击坐标：[横表情][竖表情]\n'
    return ret
def topInfo(pilot):
    return '\ntop...\n'

def initBattle(pilot):
    enflight = randomLocation()
    myflight = randomLocation()
    pilot.battle.enflight = str(enflight)
    pilot.battle.myflight = str(myflight)
    pilot.battle.save()

    sf = showFeijiFire(myflight[0],myflight[1],myflight[2], {})

    return ''.join(sf)
def feiji(player, rec):
    pilot = None
    try:
        pilot = Pilot.objects.get(wxoid = player.wxoid)
    except Pilot.DoesNotExist:
        bt = Battle(wxoid=player.wxoid)
        bt.save()
        pilot = Pilot(wxoid=player.wxoid, battle=bt, status=0, best=999)

    if pilot.status == 0:
        ret = initBattle(pilot)
        pilot.status = 1
        pilot.save()
        return ret
    elif pilot.status == 1:
        if pilot.battle.win == 1:
            bt = Battle(wxoid=player.wxoid)
            bt.save()
            pilot.battle = bt
            pilot.save()
            ret = initBattle(pilot)
            return ret
        ret = ''
        cbq = checkBiaoqing(rec)
        if cbq['ok']:
            ret += fire(pilot, cbq['xy'])
            ret += resultInfo(pilot)
        else:
            ret += helpInfo(pilot)
        #ret += topInfo(pilot)
        return ret

def inputBiaoqing(rec):
    ret = rec
    print type(rec)
    print rec
    rarr = rec.split(' ')
    r1 = rarr[0]
    r2 = rarr[1]
    r3 = rarr[2]
    bq = Biaoqing(name=r2, unc=r1, seq=r3)
    bq.save()

    return ret
