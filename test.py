#-*-coding:utf8;-*-
import requests
import json
url = 'http://169ol.com/Stream/User/submitLogin'
picurl = 'http://169ol.com/Stream/Code/getCode'
imagecode = '4278'
payload = {'phone':'1861570','password':'256','type':'1','imgcode':imagecode,'phoneCode':'','backurl':' '}
s=requests.Session()
headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'accept-encoding': "gzip, deflate",
    'accept-language': "en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4",
    'connection': "keep-alive",
    'content-length': "101",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'cookie': "channel=pt; PHPSESSID=v6eaintr88dk9p85a1r24lcmmehchk0i; Hm_lvt_d443b666104199a6e147e9b78a9c95fb=1493642267; Hm_lpvt_d443b666104199a6e147e9b78a9c95fb=1493647763",
    'host': "169ol.com",
    'origin': "http://169ol.com",
    'referer': "http://169ol.com/Stream/User/login",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'x-requested-with': "XMLHttpRequest",
    'cache-control': "no-cache", 
}
r=s.post(url,payload,headers=headers)

#r = requests.post(url,payload)

result = json.loads(r.content)
if result['code']==1:
    print result['message'].encode('utf-8')
    print'login OK'
    signurl = 'http://169ol.com/Stream/Sign/ajaxSign'
    r=s.get(signurl)
    result = json.loads(r.content)
    if result['status']==1:
        print result['msg'].encode('utf-8')
        print'sign OK'
    else:
        print result
        print result['msg'].encode('utf-8')
        print'sign failed'

else:
    print'login failed'
    print result['message'].encode('utf-8')
