from PyRsa.pyrsa import RsaKey
from PyRsa.pyb64 import Base64
from bs4 import BeautifulSoup as bs
from pre import updata_yaml, cfg
import requests, time, json, sys

if cfg['cookie'] != None:
    cf = input('已经获取cookie，是否重新获取？（y/n）')
    if cf == 'N' or cf == 'n':
        sys.exit(0)

t = str(round(time.time(),3))
t = int(t.replace('.',''))
rsaurl = 'http://jwsys.gdpu.edu.cn/xtgl/login_getPublicKey.html?time={}&_={}'.format(t,t-300)

#获取rsa加密公钥和登录cookies
session = requests.Session()
page = session.get(rsaurl, headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
})
cookie1 = page.cookies['JSESSIONID']
cookie2 = page.cookies['route']
cookie = 'route={}; JSESSIONID={}'.format(cookie2,cookie1)
print(cookie)
rsamod= json.loads(page.text)

#登录密码加密
rsakey = RsaKey()
modulus = rsamod['modulus']
exponent = rsamod['exponent']
rsakey.set_public(Base64().b64tohex(modulus), Base64().b64tohex(exponent))
rr = rsakey.rsa_encrypt(cfg['passwd'])
mm = Base64().hex2b64(rr)

#获取csrftoken
t = str(round(time.time(),3))
t = int(t.replace('.',''))
lgurl = 'http://jwsys.gdpu.edu.cn/xtgl/login_slogin.html?time={}'.format(t)
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Content-Type': 'application/x-www-form-urlencoded',
'Cookie': cookie,
'Origin': 'http://jwsys.gdpu.edu.cn',
'Referer': 'http://jwsys.gdpu.edu.cn/xtgl/login_slogin.html',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}
csrf = session.get(lgurl)
csrf = bs(csrf.text, "html.parser")
csrftoken = csrf.find(id="csrftoken").get("value")

#登录
postdata = {'csrftoken': csrftoken,'language': 'zh_CN', 'yhm': cfg['user'], 'mm': mm, 'mm': mm}
cookie3 = session.post(lgurl, headers=headers, data=postdata)
cookie3 = str(cookie3.request.headers['Cookie'])
updata_yaml('cookie',cookie3)