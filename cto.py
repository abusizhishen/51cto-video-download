#encoding=utf-8
import os, requests, time
from bs4 import BeautifulSoup

# 递归检查并创建文件夹
def check_or_make_dir(path):
    sep = os.path.sep
    if not os.path.exists(path):
        if path.find(sep) != -1:
            check_or_make_dir(path[0:path.rfind(sep)])
        os.mkdir(path)

# 拼凑时间
def total_time(total_time):
    show = ''
    sort = ('小时', '分钟', '秒')
    time_dict = {
        '小时': int(total_time / 3600),
        '分钟': int(total_time % 3600 / 60),
        '秒': int(total_time % 3600 % 60 % 60)
    }

    for i in sort:
        if time_dict[i] != 0:
            show += str(time_dict[i]) + i
    return show or '0秒'

def download(filename,urls):
    try:
        with open(filename, 'ab') as file:
            for url in urls:
                res = requests.get(url)
                file.write(res.content)
    except IOError as e:
        print e
    return

def login():
    url = 'http://home.51cto.com/index'
    headers = {
        'Host': 'edu.51cto.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    }

    headers = {
        "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
        "Accept - Encoding":"gzip, deflate",
        "Accept - Language":"zh - CN, zh;q = 0.9, en;q = 0.8",
        "Connection":"keep - alive",
        "DNT":"1",
        "Host":"home.51cto.com",
        "Upgrade - Insecure - Requests":"1",
        "User - Agent":"Mozilla / 5.0 (Macintosh;Intel Mac OS X 10_13_2) AppleWebKit / 537.36 (KHTML, likeGecko) Chrome/63.0.3239.84 Safari / 537.36"
    }

    response = requests.get(url, headers=headers)

    cookies = response.cookies.get_dict()
    soup = BeautifulSoup(response.text, 'html.parser')
    input_hidden = soup.select('input[name="_csrf"]')
    form_csrf = input_hidden[0].get('value')

    username = raw_input('用户名或者邮箱')
    password = raw_input('密码')

    data = {
        "_csrf": form_csrf,
        "LoginForm[username]":username,
        "LoginForm[password]":password,
        "LoginForm[rememberMe]":0,
        "LoginForm[rememberMe]":1,
        "login - button":"登录"
    }


    #print form_token
    # while(True):


login()






