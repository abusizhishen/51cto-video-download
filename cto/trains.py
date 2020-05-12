# coding=utf-8
from lxml import etree
from Queue import Queue
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import json, re, cto
from models import Train, Train_course, Course_lesson
from cto import Login
login = Login()
session = login.login()

q = Queue(1000)
sql_uri = 'mysql://root:root@localhost/51cto?charset=utf8mb4'

class Wejob(object,):
    action = ('info','download')
    engine = create_engine(sql_uri)
    con = sessionmaker(bind=engine)

    def __init__(self):
        self.sign = None


    def train(self):
        con = self.con()
        train_id = q.get()
        while train_id:
            result = con.query(Train).filter_by(train_id=train_id).all()
            if result:
                if result[0].status:
                    train_id = q.get()
                    continue
                else :
                    train = self.get_train_info(train_id)
                    tra_id = result[0].id
            else:
                train = self.get_train_info(train_id)
                # 写入train
                tra = Train(train_id=train_id, train_name = train['name'], course_num = train['course_num'])
                con.add(tra)
                con.commit()
                tra_id = tra.id

            #保留train index page
            url = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (train_id)

            for course in train['courses']:
                if con.query(Train_course).filter_by(train_course_id=course['train_course_id']).filter_by(tra_id=tra_id).all(): continue
                tra_cou = Train_course(tra_id = tra_id, train_course_id = course['train_course_id'], course_name = course['course_name'],
                                       course_id = course['course_id'], lesson_num = course['lesson_num'], number = course['number'])
                con.add(tra_cou)
                con.commit()
                cou_id = tra_cou.id
                lessons = self.get_course_info(train_id, int(course['train_course_id']))

                for lesson in lessons:
                    lesson['course_id'] = course['course_id']
                    lesson['cou_id'] = cou_id
                    self.insert_lesson(con,lesson)
                con.query(Train_course).filter_by(id=cou_id).update({'status':1})
            con.query(Train).filter_by(train_id=train_id).update({'status':1})

            print('微职位%s爬取完成' % train_id)
            if q.qsize():
                train_id = q.get()
            else:
                print('线程退出')
    def get_download_url(self,lesson_id,video_id):
        url = 'http://edu.51cto.com//center/player/play/m3u8?lesson_id=%s&id=%d&dp=high&type=wejoboutcourse&lesson_type=course'\
              %(lesson_id,video_id)
        res = session.get(url).text
        return re.findall(r'https.*',res)

    def get_course_info(self,train_id, course_id):
        infos = []
        current_page = 1
        while(current_page):
            url  = 'http://edu.51cto.com/center/wejob/usr/course-infoajax?train_id=%d&train_course_id=%d&page=%d&size=20'\
                  %(train_id, course_id,current_page)

            res  = session.get(url).text
            data = json.loads(res)['data']
            current_page = data['current_page'] + 1 if data['current_page'] < data['count_page'] else 0
            pages = data['data']

            for m in pages:
                info = {
                    'lesson_name': m['lesson_name'],
                    'lesson_id'  : m['lesson_id'],
                    'video_id'   : m['video_id'],
                    #'video_time' : m['video_time'].split('/')
                }
                infos.append(info)
        return infos

    def get_train_info(self,train_id):
        train = {'name':self.get_train_name(train_id),'courses':[]}
        current_page = 1

        while (current_page):
            url = 'http://edu.51cto.com/center/wejob/usr/courseajax?train_id=%d&page=%d&size=1000'%\
                  (train_id,current_page)
            res = session.get(url)

            res = json.loads(res.text)['data']
            current_page = res['current_page']+1 if  res['current_page'] < res['count_page'] else 0

            for i in res['data']:
                course = {
                    'course_name':cto.filename_reg_check(i['course_name'].encode('utf-8')),
                    'train_id':i['train_id'],
                    'train_course_id':i['train_course_id'],
                    'lesson_num':i['lesson_num'],
                    'course_id' : i['course_id'],
                    'number':i['number']
                }
                train['courses'].append(course)
            train['course_num'] = res['current_item']
        return train

    def get_train_name(self,train_id):
        url = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (train_id)
        res = session.get(url).text
        soup = BeautifulSoup(res, 'html.parser')
        title = soup.find('h2', id='CourseTitle')
        if title == None:
            exit('找不到该课程')
        return title.string

    @staticmethod
    def get_trains():
        url = 'http://edu.51cto.com/center/wejob/index/list'
        resp = session.get(url)
        html = etree.HTML(resp.text)
        hrefs = html.xpath('//div[@class="main"]//a/@href')
        for i in hrefs:
            train = int(i.split('/')[-1][0:-5])
            q.put(train)

    def insert_lesson(self,con,lesson):
        lesson_id = '_'.join([str(lesson['course_id']), str(lesson['lesson_id'])])
        urls = self.get_download_url(lesson_id, lesson['video_id'])
        video_num = len(urls)
        if video_num == 0: return
        video_url = re.sub('_\d+\.', '_{}.', urls[0])
        cou_len = Course_lesson(cou_id=lesson['cou_id'], video_id=lesson['video_id'], lesson_id=lesson['lesson_id'],
                                lesson_name=lesson['lesson_name'], video_url=video_url,
                                video_num=video_num)
        con.add(cou_len)
        con.commit()
        return

def is_exists_train(train_id):
    url = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (train_id)
    res = session.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    title = soup.find('h2', id='CourseTitle')
    if title : q.put(train_id)
    else:print('%s无效' % train_id)

def run():
    Wejob.get_trains()

    for i in range(4):
        obj = Wejob()
        t = threading.Thread(target=obj.train)
        t.start()

if __name__ == '__main__':
    run()