# coding=utf-8
import cto
import datetime
import json
import os
import random
import re
import sys
import time

from lxml import html
from cto import tools, lesson as le, decory_video

reload(sys)
sys.setdefaultencoding('utf-8')


class Wejob(object, ):
    action = ('info', 'download')

    def __init__(self, session, path='学习'):
        self.session = session
        self.train_id = 0
        self.path = tools.join_path(tools.main_path(), path)

    def train(self, train_id):
        self.train_id = train_id
        train_start = time.time()
        train = self.get_train_info()
        train_name = train['name']
        self.path += '/' + train_name
        cto.check_or_make_dir(self.path)

        print('微职位名称:' + train_name + '\n获取课程列表')
        courses = train['courses']

        total_course = len(courses)
        print('总计%d门course' % total_course)

        # 打印course名称
        for course in courses:
            print(str(courses.index(course) + 1) + '.' + course['course_name'])

        action = raw_input('是否下载y/n? 默认y:')
        if action == 'n':
            print '终止下载,程序退出'
            exit()
        # 保留train index page
        url = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (self.train_id)
        resp = self.session.get(url)
        with open(self.path + '/index.html', 'ab') as f:
            f.write(resp.content)
        # 将课程信息保存到json中去
        with open(self.path + '/info.json', 'w') as f:
            data = json.dumps(courses, ensure_ascii=False, indent=2)
            f.write(data)

        for course in courses:
            course_id = int(course['train_course_id'])
            course_index = courses.index(course) + 1

            file_path = os.path.join(self.path, course['number'] + '.' + course['course_name'])
            cto.check_or_make_dir(file_path)

            train_introduce = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (self.train_id)
            train_page = self.session.get(train_introduce)
            with open(file_path + '/index.html', 'ab') as f:
                f.write(train_page.content)

            print('%d/%d获取%s详情' % (course_index, total_course, course['course_name']))
            lessons = self.get_course_info(course_id)
            total_lesson = len(lessons)

            for lesson in lessons:
                lesson_id = '_'.join([str(course_id), str(lesson['lesson_id'])])
                lesson_index = lessons.index(lesson) + 1
                filename = os.path.join(file_path, "%d.%s.ts" % (lesson_index, lesson['lesson_name']))
                if os.path.exists(filename):
                    continue

                print datetime.datetime.now().strftime("%H:%M:%S") + ' 正在下载(%d/%d)-%s' % (
                    lesson_index, total_lesson, lesson['lesson_name'])
                try:
                    urls, get_key_url = self.get_download_url(lesson_id, lesson['video_id'])
                except Exception as e:
                    print ("解析m3u8地址保存，可能视频不存在")
                    continue
                #print "lession_id", course_id," get key url:", get_key_url
                play_key = le.Lesson(self.session).get_key_for_wejob(lesson_id, course_id,get_key_url)

                def func_decode(video_data):
                    #print "play_key:%s, lesson_id:%s, " % (play_key, lesson['lesson_id'])
                    return decory_video.Video().decory(play_key, lesson_id, video_data)

                try:
                    cto.download(filename, urls, func_decode=func_decode)
                except Exception:
                    time.sleep(random.uniform(5, 10))
                    cto.download(filename, urls)

        print 'train下载用时总计' + cto.total_time(time.time() - train_start)

    def get_download_url(self, lesson_id, video_id):
        url = 'http://edu.51cto.com//center/player/play/m3u8?lesson_id=%s&id=%d&dp=high&type=wejoboutcourse&' \
              'lesson_type=course' \
              % (lesson_id, video_id)
        res = self.session.get(url).text
        return re.findall(r'https.*', res),  "http://edu.51cto.com/"+res.split("#")[6].split(",")[1].split('"')[1]

    def get_course_info(self, course_id):
        infos = []
        current_page = 1
        while (current_page):
            url = 'https://edu.51cto.com/center/wejob/user/course-info-ajax?&train_course_id=%d&page=%d&size=20' % (
                course_id, current_page)
            res = self.session.get(url).text
            data = json.loads(res)['data']
            current_page = data['current_page'] + 1 if data['current_page'] < data['count_page'] else 0
            pages = data['data'][0]['list']

            # 判断list里的数据是list还是dict
            f = lambda m, pages: pages[m] if type(pages) is dict else m
            for m in pages:
                m = f(m, pages)
                lesson_name = m[u'lesson_name']
                lesson_name = cto.filename_reg_check(lesson_name)
                info = {
                    'lesson_name': lesson_name,
                    'lesson_id': m['lesson_id'],
                    'video_id': m['video_id']
                }
                infos.append(info)
        return infos

    def get_train_info(self):
        train = {'name': self.get_train_name(), 'courses': []}
        current_page = 1

        while (current_page):
            url = 'https://edu.51cto.com/center/wejob/user/train-course-ajax?train_id=%d&page=%d&size=20' % \
                  (self.train_id, current_page)
            res = self.session.get(url)

            try:
                res = json.loads(res.text)
            except ValueError as e:

                print "接口响应异常", "%s" % e
                print res.text
                exit()

            res = res['data']
            current_page = res['current_page'] + 1 if res['current_page'] < res['count_page'] else 0

            for i in res['data']:
                course = {
                    'course_name': cto.filename_reg_check(i['course_name'].encode('utf-8')),
                    'train_id': i['train_id'],
                    'train_course_id': i['train_course_id'],
                    'lesson_num': i['lesson_num'],
                    'number': i['sort']  # 课程的序号
                }
                train['courses'].append(course)
        return train

    def get_train_name(self):
        url = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (self.train_id)
        res = self.session.get(url)
        tree = html.fromstring(res.text)
        title = tree.xpath("//div[@class='basismes']/div")[0].get("title")
        print title

        if title == None:
            exit('找不到该课程')
        return cto.filename_reg_check(title)

    def show_train_course_list(self):
        train = self.get_train_info()
        for i in train['courses']:
            print('微职位_id: %d; 课程名称: %s ; 总课程数: %d' % (i['train_id'], i['course_name'], i['lesson_num']))
        return

    def get_train_id_by_list(self):
        url = 'https://edu.51cto.com/center/wejob/center/trains?page=%d&size=1000'
        resp = self.session.get(url % 1).text
        resp_json = json.loads(resp)

        data = resp_json['data']
        if len(data) == 0:
            exit("没有查询到微职位")
        data = data['data']

        print "以下是您购买的微职位"
        print

        train_desc = []
        for i in data:
            train_desc.append(int(i['train_id']))
            print i['train_id'], i['name']
            print
            print "课程id: %d, 课程名称: %s" % (int(i['train_id']), i['name'])

        print

        while True:
            try:
                input = raw_input("请输入您要下载的微职位id:")
                input = int(input)
            except ValueError:
                print "无效的输入:", input
            else:
                if input in train_desc:
                    return input
                else:
                    if input == 0:
                        exit(0)
                    print "课程id无效:", input
