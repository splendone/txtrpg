#coding=utf-8
from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)
# Create your views here.


import hashlib
import json
from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from auto_reply.views import auto_reply_main # 修改这里
# from auto_reply.views import auto_reply_test

WEIXIN_TOKEN = 'test329'

@csrf_exempt
def checkSignature(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        logger.info(signature)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    else:
        xml_str = smart_str(request.body)
        print xml_str
        request_xml = etree.fromstring(xml_str)
        return auto_reply_main(request, request_xml)


@csrf_exempt
def test(request):
    reccont = request.GET.get("reccont", None)
    wxoid = request.GET.get("wxoid", None)
    print wxoid
    print reccont
    return auto_reply_test(request, wxoid, reccont)

def fc(request):
    con = '''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <html>
     <head>
       <title> New Document </title>
         <meta name="Generator" content="EditPlus">
           <meta name="Author" content="">
             <meta name="Keywords" content="">
               <meta name="Description" content="">
                </head>

                 <body>
                   <div>
                       <div id="emulator">
                               <p>To play this game, please, download the latest Flash player!</p>
                                       <br>
                                               <a href="http://www.adobe.com/go/getflashplayer">
                                                           <img src="//www.adobe.com/images/shared/download_buttons/get_adobe_flash_player.png" alt="Get Adobe Flash player"/>
                                                                   </a>
                                                                       </div>
                                                                       </div>

                                                                       <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
                                                                       <script src="//ajax.googleapis.com/ajax/libs/swfobject/2.2/swfobject.js"></script>

                                                                       <script type="text/javascript">

                                                                           var resizeOwnEmulator = function(width, height)
                                                                               {
                                                                                       var emulator = $('#emulator');
                                                                                               emulator.css('width', width);
                                                                                                       emulator.css('height', height);
                                                                                                           }

                                                                                                               $(function()
                                                                                                                   {
                                                                                                                           function embed()
                                                                                                                                   {
                                                                                                                                               var emulator = $('#emulator');
                                                                                                                                                           if(emulator)
                                                                                                                                                                       {
                                                                                                                                                                                       var flashvars = 
                                                                                                                                                                                                       {
                                                                                                                                                                                                                           system : 'sega',
                                                                                                                                                                                                                                               url : '/roms/Flappy Bird (PD) v1.0.gen'
                                                                                                                                                                                                                                                               };
                                                                                                                                                                                                                                                                               var params = {};
                                                                                                                                                                                                                                                                                               var attributes = {};

                                                                                                                                                                                                                                                                                                               params.allowscriptaccess = 'sameDomain';
                                                                                                                                                                                                                                                                                                                               params.allowFullScreen = 'true';
                                                                                                                                                                                                                                                                                                                                               params.allowFullScreenInteractive = 'true';

                                                                                                                                                                                                                                                                                                                                                               swfobject.embedSWF('flash/Nesbox.swf', 'emulator', '640', '480', '11.2.0', 'flash/expressInstall.swf', flashvars, params, attributes);
                                                                                                                                                                                                                                                                                                                                                                           }
                                                                                                                                                                                                                                                                                                                                                                                   }

                                                                                                                                                                                                                                                                                                                                                                                           embed();
                                                                                                                                                                                                                                                                                                                                                                                               });

                                                                                                                                                                                                                                                                                                                                                                                               </script>
                                                                                                                                                                                                                                                                                                                                                                                                </body>
                                                                                                                                                                                                                                                                                                                                                                                                </html>

    '''
    return HttpResponse(con)
    
