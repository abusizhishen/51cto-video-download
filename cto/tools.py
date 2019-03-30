#encoding=utf-8
import sys, json, pickle, requests, re
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')
import os, requests

# 递归检查并创建文件夹
def check_or_make_dir(path):
    sep = os.path.sep
    if not os.path.exists(path):
        if path.find(sep) != -1:
            check_or_make_dir(path[0:path.rfind(sep)])
        os.mkdir(path)

# 拼凑时间 total_time单位为秒
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

#下载并保存文件
def download(filename,urls):
    try:
        with open(filename, 'ab') as file:
            for url in urls:
                res = requests.get(url)
                file.write(res.content)
    except IOError as e:
        print(e)
    return


def filename_reg_check(filename):
    return re.sub('[\?\*\/\\\!]', '&', filename)


# 获取“当前”文件所在目录
def get_current_path(current_file):
    return os.path.split(os.path.realpath(current_file))[0]


# 获取当前文件所在目录的父目录
def get_current_dirpath(current_path):
    return os.path.dirname(get_current_path(current_path))
