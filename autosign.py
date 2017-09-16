# -*- coding:utf-8 -*-
from learnRecSVM import predict
from PIL import Image
import requests
import json
import smtplib



url = 'http://169ol.com/Stream/User/submitLogin'
imgUrl = 'http://169ol.com/Stream/Code/getCode'

head = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'accept-encoding': "gzip, deflate",
    'accept-language': "en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4",
    'connection': "keep-alive",
    'content-length': "101",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'host': "169ol.com",
    'origin': "http://169ol.com",
    'referer': "http://169ol.com/Stream/User/login",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'x-requested-with': "XMLHttpRequest",
    'cache-control': "no-cache"
}
rhead = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, sdch",
    'connection': "keep-alive",
    'host': "169ol.com",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'cache-control': ""
}


def sign(phone, pswd):
    s = requests.session()
    msg=''
    # 验证码
    imagecode = ''
    retry = 0
    while (True):
        vimg = s.get(imgUrl, headers=rhead)
        # save image to disk
        with open('code.png', 'wb') as f:
            f.write(vimg.content)
        #imagecode = split_rec.rec_img('code.png')
        imagecode = "".join(predict('code.png'))
        retry = retry + 1
        if retry>20:
            msg='faild to get the validation code, tried 10 times'
            return msg
        if(len(imagecode)!=4):
            continue

        payload = {'phone': phone,
                   'password': pswd,
                   'type': '1',
                   'imgcode': imagecode,
                   'phoneCode': '', 'backurl': ' '}

        r = s.post(url, data=payload, headers=head)
        print r.text.encode('utf-8')
        result = json.loads(r.content)
        msg = result['message'].encode('utf-8')
        if msg=='图形验证码错误':
            continue

        if result['code'] == 1:
            print result['message'].encode('utf-8')
            print'login OK'
            signurl = 'http://169ol.com/Stream/Sign/ajaxSign'
            r = s.get(signurl)
            result = json.loads(r.content)
            msg = result['msg'].encode('utf-8')
            if result['status'] == 1:

                print'sign OK'
            else:
                print'sign failed'

        else:
            print'login failed'

        return msg

fname = "userdata.txt"
with open(fname) as f:
    content = f.readlines()
content = [x.strip() for x in content]
for usr in content:
    udata=usr.split(",")
    phone = udata[0]
    pswd = udata[1]
    email = udata[2]
    try:
        returnmsg = sign(phone,pswd)
        print returnmsg

    except Exception,e:
        print ('签到异常 '+' error:'+ str(e.message) )
