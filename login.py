#encoding=utf-8
import requests, sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup

def login():
    url = 'http://home.51cto.com/index'
    headers = {
        'Host': 'home.51cto.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    }

    session = requests.Session()
    response = session.get(url, headers=headers)

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control":"max-age=0",
        "Content-Length":"230",
        "Content-Type":"application/x-www-form-urlencoded",
        "Cookie":"acw_tc=AQAAAJ0TuXgq9QkAdbkwPbW6x915NaJK;PHPSESSID=f2afs83hvd0d9960pr6dcn8dh1;_csrf=dd6cb7ea9b3d20bf447baed9d6b54f84916d359861ddc0c823fb74fe787792b3a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22uwc9v4gS3ygV8-J04xNtoJNHzj48AIU1%22%3B%7D; _ourplusFirstTime=117-12-23-23-29-29; _ourplusReturnTime=117-12-23-23-29-29; _ourplusReturnCount=1; www51cto=5FB0606C864B7789B0AA18C862DA3D49AsYV; Cto_lvt_=1514025050,1514041061,1514041134,1514042969; Cto_lpvt_=1514042969; Cto_uid_=0",
        "DNT":"1",
        "Host":"home.51cto.com",
        "Origin":"http://home.51cto.com",
        "Proxy-Connection":"keep-alive",
        "Referer":"http://home.51cto.com/index",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    }

    soup = BeautifulSoup(response.text, 'html.parser')
    csrf = soup.find('input', {'name':'_csrf'})

    # username = raw_input('用户名或者邮箱:')
    # password = raw_input('密码:')
    username = 'abusizhishen'
    password = 'lby123456789'

    data = {
        "_csrf":csrf,
        "LoginForm[username]":"abusizhishen",
        "LoginForm[password]":"lby123456789",
        "LoginForm[rememberMe]":"0",
        "login-button":"登 录"
    }

    res = requests.post(url,data=data,headers=headers)
    print(res.text)
    # #exit()
    # with open('../login.html','w+') as f:
    #     f.write(res.text)

    url = 'http://edu.51cto.com/center/user/sign/index'
    #res=session.get(url,headers=headers)
    #print(res.text)
    # with open('../kk.html','w+') as f:
    #     f.write(res.text)

login()