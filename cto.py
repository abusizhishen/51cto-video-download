#encoding=utf-8
import os,requests, threading, time

# 递归检查并创建文件夹
def check_or_make_dir(path):
    if not os.path.exists(path):
        if path.find('/') != -1:
            check_or_make_dir(path[0:path.rfind('/')])
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
    with open(filename, 'ab') as file:
        for url in urls:
            res = requests.get(url)
            file.write(res.content)
    return

class  MulGet (object):
    result = {}
    def __init__(self,urls):
        self.urls = urls
        self.urls_bak = urls

    def do(self):
        while self.urls:
            url = self.urls.pop()
            self.result[time.time()] = requests.get('http://www.hao123.com')
            print '当前线程名%s' % (threading.currentThread().name)
            time.sleep(2)
    def moive(self):
        for i in range(5):
            print '我在看电影,当前线程名%s' % (threading.currentThread().name)
            time.sleep(3)

    def music(self):
        for i in range(5):
            print '我在听音乐,当前线程名%s' % (threading.currentThread().name)
            time.sleep(3)

    def eat(self):
        for i in range(5):
            print '我在吃饭,当前线程名%s' % (threading.currentThread().name)
            time.sleep(3)

    def tea(self):
        for i in range(5):
            print '我在喝茶,当前线程名%s' % (threading.currentThread().name)
            time.sleep(3)

    def mkThread(self):
        t1 = threading.Thread(target=self.moive())
        t2 = threading.Thread(target=self.tea())
        t3= threading.Thread(target=self.music)
        t4 = threading.Thread(target=self.eat())

        threads = []

        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        threads.append(t4)

        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()

    def back(self):
        content = ''
        print self.result
        for i in self.result:
            content += i

        return content

if __name__ == '__main__':
    urls = range(10)
    obj = MulGet(urls)
    obj.mkThread()
    re = obj.back()
    print re