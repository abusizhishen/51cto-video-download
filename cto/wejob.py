# coding=utf-8
from bs4 import BeautifulSoup
import json,re,os,time,random,datetime,sys,cto
from cto import Login
reload(sys)
sys.setdefaultencoding('utf-8')


class Wejob(object,):
    action = ('info', 'download')

    def __init__(self, train_id, path = '学习'):
        login = Login()
        self.session = login.login()
        self.train_id = train_id
        current_path = os.path.abspath(__file__)
        self.path = os.path.abspath(os.path.join(current_path,'../../../',path))

    def train(self):
        train_start = time.time()
        train = self.get_train_info()
        train_name = train['name']
        self.path+='/'+train_name
        cto.check_or_make_dir(self.path)

        print('微职位名称:'+train_name+'\n获取课程列表')
        courses = train['courses']

        total_course = len(courses)
        print('总计%d门course' % (total_course))
        #打印course名称
        for course in courses:
            print(str(courses.index(course)+1)+'.'+course['course_name'])

        action = raw_input('是否下载y/n? 默认y:')
        if action == 'n':
            print '终止下载,程序退出'
            exit()
        #保留train index page
        url = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (self.train_id)
        resp =self.session.get(url)
        with open(self.path+'/index.html', 'ab') as f:
            f.write(resp.content)
        #将课程信息保存到json中去
        with open(self.path +'/info.json','w') as f:
            data = json.dumps(courses, ensure_ascii=False, indent=2)
            f.write(data)

        for course in courses:
            course_id = int(course['train_course_id'])
            course_index = courses.index(course)+1

            file_path = os.path.join(self.path, course['number']+'.'+course['course_name'])
            cto.check_or_make_dir(file_path)

            train_introduce = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (self.train_id)
            train_page =self.session.get(train_introduce)
            with open(file_path+'/index.html', 'ab') as f:
                f.write(train_page.content)

            print('%d/%d获取%s详情' % (course_index, total_course,course['course_name']))
            lessons = self.get_course_info(course_id)
            total_lesson = len(lessons)

            for lesson in lessons:
                lesson_id = '_'.join([str(course_id), str(lesson['lesson_id'])])
                lesson_index = lessons.index(lesson)+1
                filename = os.path.join(file_path, "%d.%s.ts" % (lesson_index, lesson['lesson_name']))
                if os.path.exists(filename):
                    continue

                print datetime.datetime.now().strftime("%H:%M:%S")+' 正在下载(%d/%d)-%s' % (lesson_index,total_lesson,lesson['lesson_name'])
                urls = self.get_download_url(lesson_id, lesson['video_id'])
                try:
                    cto.download(filename, urls)
                except Exception :
                    time.sleep(random.uniform(5,10))
                    cto.download(filename, urls)

        print 'train下载用时总计'+cto.total_time(time.time()-train_start)

    def get_download_url(self,lesson_id,video_id):
        url = 'http://edu.51cto.com//center/player/play/m3u8?lesson_id=%s&id=%d&dp=high&type=wejoboutcourse&lesson_type=course'\
              %(lesson_id,video_id)
        res = self.session.get(url).text
        return re.findall(r'https.*',res)

    def get_course_info(self, course_id):
        infos = []
        current_page = 1
        while(current_page):
            url = 'http://edu.51cto.com/center/wejob/usr/course-infoajax?train_id=%d&train_course_id=%d&page=%d&size=20'\
                  % (self.train_id, course_id,current_page)
            res = self.session.get(url).text
            data = json.loads(res)['data']
            current_page = data['current_page'] + 1 if data['current_page'] < data['count_page'] else 0
            pages = data['data']

            for m in pages:
                info = {
                    'lesson_name': cto.filename_reg_check(m['lesson_name']),
                    'lesson_id': m['lesson_id'],
                    'video_id': m['video_id']
                }
                infos.append(info)
        return infos

    def get_train_info(self):
        train = {'name':self.get_train_name(),'courses':[]}
        current_page = 1

        while (current_page):
            url = 'http://edu.51cto.com/center/wejob/usr/courseajax?train_id=%d&page=%d&size=1000'%\
                  (self.train_id,current_page)
            res = self.session.get(url)
            res = json.loads(res.text)['data']
            current_page = res['current_page']+1 if  res['current_page'] < res['count_page'] else 0

            for i in res['data']:
                course = {
                    'course_name':cto.filename_reg_check(i['course_name'].encode('utf-8')),
                    'train_id':i['train_id'],
                    'train_course_id':i['train_course_id'],
                    'lesson_num':i['lesson_num'],
                    'number':i['number']
                }
                train['courses'].append(course)
        return train

    def get_train_name(self):
        url = 'http://edu.51cto.com/center/wejob/index/view?id=%d&force=3&orig=try' % (self.train_id)
        res = self.session.get(url).text
        soup = BeautifulSoup(res, 'html.parser')
        title = soup.find('h2', id='CourseTitle')
        if title == None:
            exit('找不到该课程')
        return cto.filename_reg_check(title.string)

    def show_train_course_list(self):
        train = self.get_train_info()
        for i in train['courses']:
            print('微职位_id: %d; 课程名称: %s ; 总课程数: %d' % (i['train_id'],i['course_name'], i['lesson_num']))
        return