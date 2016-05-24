#coding=utf-8
from django.shortcuts import render
#from txtadventure.models import Player
#from txtadventure.player import Player as PP
import urllib2,urllib
import json
import random
import datetime
import time

# Create your views here.
def xiaohua():
    dt7 = datetime.date.today() - datetime.timedelta(days=1)
    tt7 = dt7.timetuple()
    ts7 = time.mktime(tt7)
    url = "http://japi.juhe.cn/joke/content/list.from?key=7002d5690f309a124a179936155e0660&page=1&pagesize=50&sort=asc&time={}".format(str(int(ts7)))

    #url = "http://japi.juhe.cn/joke/content/text.from?key=7002d5690f309a124a179936155e0660&page=1&pagesize=20"
    print url
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    l = len(data['result']['data'])
    rk = random.randint(0,l-1)
    ret = data['result']['data'][rk]['content']
    ret = ret.replace('"', '\"').replace(' ','')
    return ret
    pass
def historyToday():
    url = "http://v.juhe.cn/todayOnhistory/queryEvent.php?key=54e4fb6ed420cc2fcb12a39ada419d64&date={}/{}".format(str(datetime.date.today().month), str(datetime.date.today().day))
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    ret = ''
    if data['reason'] == 'success':
        l = len(data['result'])
        rk = random.randint(0,l-1)
        dt = data['result'][rk]['date']
        ttl = data['result'][rk]['title']
        eid = data['result'][rk]['e_id']
        print eid
        print type(eid)
        detail_url = 'http://v.juhe.cn/todayOnhistory/queryDetail.php?key=54e4fb6ed420cc2fcb12a39ada419d64&e_id={}'.format(eid)
        detail_response = urllib.urlopen(detail_url)
        detail_data = json.loads(detail_response.read())
        dtl = detail_data['result'][0]['content']
        print dtl
        ret += '\n日期:{}\n标题:{}\n详情:{}\n'.format(dt,ttl,dtl)


        #for k in range(l):
        #    dt = data['result'][k]['date']
        #    ttl = data['result'][k]['title']
        #    print dt
        #    print ttl
        pass

    return ret
    pass
def wifi(rec):
    print rec
    print type(rec)
    bdurl = "http://api.map.baidu.com/geoconv/v1/?coords={},{}&from=3&to=5&ak=rY4zy9so9MogGdecwdT9NSfS".format(rec[-1],rec[0])
    bdresponse = urllib.urlopen(bdurl)
    bddata = json.loads(bdresponse.read())
    print bddata
    x = bddata['result'][0]['x']
    y = bddata['result'][0]['y']
    print x
    print y

    url = "http://apis.juhe.cn/wifi/local?key=7069d0a4912e820c35f22b8b0b65668f&lon={}&lat={}&r=500&type=1".format(x,y)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    print data
    ret = ''
    if data['resultcode'] == '200':
        datas = data['result']['data']
        print '!!!!!!!!!!!!!!!!!!!!!!'
        print datas
        for k in range(len(datas)):
            if k > 5:
                break

            name = datas[k]['name']
            intro = datas[k]['intro']
            address = datas[k]['address']
            distance = datas[k]['distance']
            ret += '\n====[{}]====\n介绍:{}\n地址:{}\n距离:{}\n\n'.format(name, intro, address, distance)
        pass
    print '@@@@@@@@@@@@@@@@'
    print ret
    return ret

    pass
def chengyu(keyword):
    print type(keyword)
    print dir(keyword)
    f = {'key':'fec54f6d8d0255853863eb4b13b2b0fb', 'word':str(keyword)}
    keyword = urllib.urlencode(f)
    print keyword
    url = "http://v.juhe.cn/chengyu/query?{}".format(keyword)
    #keyword = urllib.urlencode(keyword.encode('utf8'))
    #url = "http://v.juhe.cn/chengyu/query?key=fec54f6d8d0255853863eb4b13b2b0fb&word={}".format(keyword)
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    #req = urllib2.Request("http://v.juhe.cn/chengyu/query?key=fec54f6d8d0255853863eb4b13b2b0fb&word={}".format(keyword))
    #opener = urllib2.build_opener()
    #f = opener.open(req)
    #json = json.loads(f.read())
    #rt = json.dumps(data['result'])
    rt = str(data['result'])
    if data['reason'] == 'success':
        rt = '拼音：{}\n成语解释：{}\n同义词：{}\n反义词：{}\n'.format(data['result']['pinyin'],data['result']['chengyujs'],formatString(data['result']['tongyi']), formatString(data['result']['fanyi']))
        print rt
    else:
        rt = '不是成语？？'
    return rt
    pass
def formatString(s):
    return str(s).decode("unicode-escape").encode("utf-8").replace('\'', '').replace('u', '')
    pass
