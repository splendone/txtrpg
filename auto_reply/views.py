#coding=utf-8
from django.shortcuts import render
from txtadventure.models import Player, Maps, Tiles, Enemies, Items#, ItemTypes


# from txtadventure import world
from txtadventure import actions
from txtadventure.player import Player as PP
# world.load_tiles()
from txtadventure.utils import help_info,hotkey_info

from juhe.views import chengyu, wifi ,historyToday,xiaohua
from dafeiji.views import feiji

import time
import random

# Create your views here.
from django.http import HttpResponse


DEBUG_FLAG = False
START_LOCATION = (0,0)

CHENGYU = 1900 
WIFI = 1901 
FEIJI = 2700


def auto_reply_main(request, request_xml):
    toUser =  request_xml.find('ToUserName').text
    fromUser = request_xml.find('FromUserName').text
    createTime = int(time.time())
    # msgType = request_xml.find('MsgType').text 
    #receiveContent = request_xml.find('Content').text
    msgType = request_xml.find('MsgType').text
    print msgType
    receiveContent = ''
    if msgType == 'text':
        receiveContent = request_xml.find('Content').text
    elif msgType == 'location':
        receiveContent = (request_xml.find('Location_X').text, request_xml.find('Location_Y').text)
        print receiveContent
        pass
    
    print receiveContent

##############
# def auto_reply_test(request, fromUser, receiveContent):
    
#     request_xml = ''
##############
    print request_xml
    resContent = ''
    player = None
    try:
        player = Player.objects.get(wxoid=fromUser)
    except Player.DoesNotExist:
        print '没找到用户账号'
        player = None
        
    if player == None:
        print '创建新用户...'
        # maps = None
        # try:
        #     maps = Maps.objects.get(id=1)
        # except Maps.DoesNotExist:
        #     maps = Maps(name='world1', desc='this is the first world.', level=1, enter='{}')
        #     maps.save()
        
        maps = Maps(name='world1', wxoid=fromUser, desc='this is the first world.', level=1, enter='{}')
        maps.save()
        player = Player(wxoid=fromUser, inmap=maps)
        player.save()
        
        resContent += '''(请输入你的名字)'''
        if DEBUG_FLAG:
            return HttpResponse(resContent)
        else:
            return reply_text(request, request_xml, resContent)
    else:
        print player.status
        if receiveContent.lower() == 'h2d':
            resContent = historyToday()
            if DEBUG_FLAG:
                return HttpResponse(resContent)
            else:
                return reply_text(request, request_xml, resContent)
            pass
        if receiveContent.lower() == 'xh':
            resContent = xiaohua()
            if DEBUG_FLAG:
                return HttpResponse(resContent)
            else:
                return reply_text(request, request_xml, resContent)
            pass
        if receiveContent == '??':
            resContent = '全部快捷键：（待完善）'
            if DEBUG_FLAG:
                return HttpResponse(resContent)
            else:
                return reply_text(request, request_xml, resContent)
            pass
            
        if player.status == 0:
            player.name = receiveContent
            player.status = 1
            player.location_x, player.location_y = START_LOCATION
            player.save()
            
            try:
                maps = Maps.objects.get(wxoid=fromUser)
                maps.name = "{} 的世界".format(receiveContent)
                maps.save()
            except Maps.DoesNotExist:
                pass
            
            pp = PP(player)
            # return help_info(pp,resContent)
            resContent += '你好啊，【{}】'.format(receiveContent)
            resContent = help_info(pp,resContent)
            resContent += '\n【便民工具之成语词典】\n输入6cy，可以查成语词典\n'
            if DEBUG_FLAG:
                return HttpResponse(resContent)
            else:
                return reply_text(request, request_xml, resContent)
        elif player.status == CHENGYU:
            print receiveContent
            if receiveContent.lower() == 'cy4':
                resContent = '已经关闭词典。打开成语词典请输入：6cy'
                player.status = 1
                player.save()
                if DEBUG_FLAG:
                    return HttpResponse(resContent)
                else:
                    return reply_text(request, request_xml, resContent)
                pass
            else:
                resContent = chengyu(receiveContent)
                resContent += '\n退出成语词典：cy4\n'
                if DEBUG_FLAG:
                    return HttpResponse(resContent)
                else:
                    return reply_text(request, request_xml, resContent)
                pass
        elif player.status == WIFI:
            if receiveContent.lower() == 'wifi4':
                resContent = '关闭wifi'
                player.status = 1
                player.save()
                if DEBUG_FLAG:
                    return HttpResponse(resContent)
                else:
                    return reply_text(request, request_xml, resContent)
                pass
            resContent = wifi(receiveContent)
            resContent += '\nexit: wifi4\n'
            if DEBUG_FLAG:
                return HttpResponse(resContent)
            else:
                return reply_text(request, request_xml, resContent)
            pass
        elif player.status == FEIJI:
            if receiveContent.lower() == 'feiji4':
                resContent = '关闭FEIJI'
                player.status = 1
                player.save()
                if DEBUG_FLAG:
                    return HttpResponse(resContent)
                else:
                    return reply_text(request, request_xml, resContent)
                pass
            resContent = feiji(player, receiveContent)
            resContent += '\nexit: feiji4\n'
            if DEBUG_FLAG:
                return HttpResponse(resContent)
            else:
                return reply_text(request, request_xml, resContent)
            pass
        #else:
        elif player.status == 1:
            pp = PP(player)
            if receiveContent.lower() == 'h':
                # return help_info(pp, resContent)
                resContent = help_info(pp, resContent)
                if DEBUG_FLAG:
                    return HttpResponse(resContent)
                else:
                    return reply_text(request, request_xml, resContent)
            elif receiveContent.lower() == '6cy':
            #进入‘成语’
                player.status = CHENGYU
                player.save()
                resContent = '请输入要查询的成语:\n(关闭成语词典输入：cy4)'
                #resContent = chengyu(player, 1)
                if DEBUG_FLAG:
                    return HttpResponse(resContent)
                else:
                    return reply_text(request, request_xml, resContent)
                pass
            elif receiveContent.lower() == '6wifi':
                player.status = WIFI
                player.save()
                resContent = '发送位置，查找周边wifi，关闭wifi请输入：wifi4'
                if DEBUG_FLAG:
                    return HttpResponse(resContent)
                else:
                    return reply_text(request, request_xml, resContent)
                pass
            elif receiveContent.lower() == '6feiji':
                player.status = FEIJI
                player.save()
                resContent = '关闭FEIJI请输入：feiji4'
                if DEBUG_FLAG:
                    return HttpResponse(resContent)
                else:
                    return reply_text(request, request_xml, resContent)
                pass
            else:
                # return hotkey_info(pp, resContent, receiveContent)
                
                resContent = hotkey_info(pp, resContent, receiveContent)
                if DEBUG_FLAG:
                    return HttpResponse(resContent)
                else:
                    return reply_text(request, request_xml, resContent)




#########################################
##################################################################################
###########################################################################################################################
##################################################################################
###########################################################################################################################
##################################################################################
#########################################




# def auto_reply_main(request, request_xml):
#     toUser =  request_xml.find('ToUserName').text
#     fromUser = request_xml.find('FromUserName').text
#     createTime = int(time.time())
#     # msgType = request_xml.find('MsgType').text 
#     receiveContent = request_xml.find('Content').text
# ###############
# # def auto_reply_test(request, fromUser, receiveContent):
# ###############
#     resContent = ''
#     try:
#         player = Player.objects.get(wxoid=fromUser)
#     except Player.DoesNotExist:
#         player = None
        
#     if not player:
#         print '创建新用户...'
#         player = Player(wxoid=fromUser)
#         player.save()
        
#         resContent += '''你发现自己在一个洞里，墙壁上插着火把，火焰跳跃着，四周有通道，漆黑而充满未知……
#                 你揉着昏沉沉的头，努力回想自己是谁，却只能依稀记得自己的名字是……
#                 （请输入你的名字）'''
#         # return HttpResponse(resContent)
#         return reply_text(request, request_xml, resContent)
#     else:
#         if player.status == 0:
#             player.name = receiveContent
#             player.status = 1
#             player.location_x, player.location_y = world.starting_position
#             player.save()
#             pp = PP(player)
#             # return help_info(pp,resContent)
#             resContent = help_info(pp,resContent)
#             return reply_text(request, request_xml, resContent)
#         elif player.status == 1:
#             pp = PP(player)
#             if pp.victory:
#                 pp.status = 2
#                 pp.save()
#                 resContent = 'you win!'
#                 # return HttpResponse(resContent)
#                 return reply_text(request, request_xml, resContent)
#             if receiveContent == '?':
#                 # return help_info(pp, resContent)
#                 resContent = help_info(pp, resContent)
#                 return reply_text(request, request_xml, resContent)
#             else:
#                 # return hotkey_info(pp, resContent, receiveContent)
#                 resContent = hotkey_info(pp, resContent, receiveContent)
#                 return reply_text(request, request_xml, resContent)
#         elif player.status == 2:
#             if player.victory:
#                 resContent = win_info(pp, resContent)
#                 return reply_text(request, request_xml, resContent)
#             else:
#                 resContent = lose_info(pp, resContent)
#                 return reply_text(request, request_xml, resContent)
#         pass




def reply_text(request, request_xml, resContent):
    toUser =  request_xml.find('ToUserName').text
    fromUser = request_xml.find('FromUserName').text
    createTime = int(time.time())
    return render(request, 'reply_text.xml', {'toUser': fromUser, 'fromUser': toUser, 'createTime': createTime, 'content': resContent}, content_type="application/xml")



