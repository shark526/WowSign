# -*- coding:utf-8 -*-
import requests
import random
import json

signUrl = "http://wxsc1.unisk.cn/WeiXinSC/signIn?b="+ str(random.uniform(0.0, 1.0))
openId = "<your open id here>"
head = {
    'Host':'wxsc1.unisk.cn',
    'Proxy-Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4',
    'Origin':'http://wxsc1.unisk.cn'
}
def sign(openId):
    exeResult = ""
    s = requests.session()
    payload = {"openid": openId,"type": 2}
    r = s.post(signUrl, data=payload, headers=head)
    print r.text.encode('utf-8')
    #print r.content
    result = json.loads(r.content)
    print result['sign']
    if (result['sign'] == '1' or result['sign'] == '2'):
       exeResult = 'already signed!'
    else:
       exeResult = 'sign failed, please check the internet!'
    return exeResult

if __name__=="__main__":
    result = sign(openId)
    print result
