#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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

    session = requests.session()
    # response = session.get(url, headers=headers)
    #
    # soup = BeautifulSoup(response.text, 'html.parser')
    # form_csrf = soup.find('input', {'name':'_csrf'})['value']
    #
    # # username = raw_input('用户名或者邮箱')
    # # password = raw_input('密码')
    # username = 'abusizhishen'
    # password = 'lby123456789'
    #
    # data = {
    #     "_csrf": form_csrf,
    #     "LoginForm[username]":username,
    #     "LoginForm[password]":password,
    #     "LoginForm[rememberMe]":0,
    #     "LoginForm[rememberMe]":1,
    #     "login - button":"登录"
    # }

    headers['Host']='home.51cto.com'
    headers['Origin'] = 'http://home.51cto.com'
    headers['Referer'] = 'http://home.51cto.com/index'
    #headers['Cache-Control'] = 'max-age=0'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Cookie'] = "acw_tc=AQAAAOG6rm7weA4A8Q9MLarwQ841R88Q; new=yes; _ourplusFirstTime=117-12-21-0-35-20; _csrf=0bca70d6ec76371b0a73b7410ee12b5ee2387b2608a21a55bdeef650c9988e67a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22%C0%9A%7F%7D%DE%AA%18Z%B6%DEp5%08%25%03i%95%D8L%88%F1%19%CC%C2n%C6%0D%7E%15%7F%AD%85%22%3B%7D; EDUACCOUNT=c5e670f018520416e4fa50de7e6ca8d6b8ac5eb675fde843851bf8760bab1d21a%3A2%3A%7Bi%3A0%3Bs%3A10%3A%22EDUACCOUNT%22%3Bi%3A1%3Bs%3A32%3A%22798d289488b69ec85ddc15e33afa70fd%22%3B%7D; 11552349new=yes; _identity=bfa70a0c76b4d639179329e98252535bc1c0703e07a646c078b24fed8572029ba%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A20%3A%22%5B1353200%2Ctrue%2C43200%5D%22%3B%7D; eduSearchkey=Pythonç½ç»ç¬è«; www51cto=91D6CE4E5717F685DFF9C8BB39C0CD1Anjxr; pub_sauth1=AAZMFwwfXwtAXFdfaghXAQEBB1BfOwQEU1cHVwZTVgQ; pub_sauth2=83bb1840ce8247ceeaa6012a64bbd043; pub_cookietime=864000; PHPSESSID=1berlot0c7gg8e4kg096587mj9; Cto_lvt_=1513787741,1514033859,1514033859; looyu_id=d01e2e25a4a07df1a339e8e13b9232dd28_20000923%3A1; 11552349flag=yes; _ourplusReturnCount=46; _ourplusReturnTime=117-12-23-22-3-5; Cto_lpvt_=1514037787"

    # res = session.post(url,data=data,headers=headers)
    # #print(res.text)
    # with open('../login.html','w+') as f:
    #     f.write(res.text)
    #
    # #print form_token
    # # while(True):

    url = 'http://edu.51cto.com/center/user/sign/index'

    data = {
        'good_id': 4773,
        'type': 1,
        'source': 1
    }

    res=requests.get(url,headers=headers)#,cookies = res.cookies.get_dict())
    print(res.text)
    with open('../kk.html','w+') as f:
        f.write(res.text)


if __name__ == '__main__':
    login()






