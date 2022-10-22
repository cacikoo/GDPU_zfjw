import requests, time, json
import yaml

from pre import cfg, tymlpath, tabulation
session = requests.Session()
year = input('输入第一学期学年')
term = input('输入学期（1/2）')
if term == '1':
    term = 3
else:
    term = 12

#获取课程表
t = str(round(time.time(),3))
t = int(t.replace('.',''))
kburl = 'http://jwsys.gdpu.edu.cn/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N253508&su={}'.format(cfg['user'])
headers = {
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
'Cookie': cfg['cookie'],
'Referer': 'http://jwsys.gdpu.edu.cn/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N253508&layout=default&su={}'.format(cfg['user']),
'User-Agent': 'Mozilla/5.0 (Windows NT 11.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5193.173 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'
}
name = year + '学年第' +term + '学期.xlsx'
pdata = {'xnm': year,'xqm': term,'kzlx': 'ck'}
kb = requests.post(kburl,headers=headers,data=pdata)
nkb = json.loads(kb.text)
with open(tymlpath,'w',encoding='utf-8') as f1:
    yaml.dump_all(nkb['kbList'],f1,default_flow_style=False, encoding='utf-8', allow_unicode=True)
tabulation(name)

