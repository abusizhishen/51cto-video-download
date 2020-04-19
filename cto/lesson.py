# encoding=utf-8
import simplejson as json, execjs, re, os
from cto import Login,tools


class Lesson(object):
    lesson_id = 0
    size = 20
    page = 1
    course_id = 0
    course_name = ""

    def __init__(self, session, path="学习"):
        self.session = session
        self.course_id = 0
        self.lesson_id = 0
        self.list = []
        self.data = []  # [['filename':'',urls:[]]]
        self.path = tools.join_path(tools.main_path(), path)

        pass

    def lesson_list(self):
        infos = []
        page = self.page

        # "lessonList":Array[7],
        #         "currentPage":4,
        #         "pageCount":4,

        while True:
            url = "https://edu.51cto.com/center/course/user/get-lesson-list?page=%d&size=%d&id=%d" % \
                  (page, self.size, self.course_id)
            resp = self.session.get(url)
            result = json.loads(resp.text)
            chapter = ""

            # resp struct
            # {
            #     "status":1,
            #     "msg":"课时列表",
            #     "data":{
            #         "lessonList":Array[25],
            #         "currentPage":1,
            #         "pageCount":3,
            #         "page":[
            #             1,
            #             2,
            #             3
            #         ],
            #         "last_lesson":{
            #             "lesson":false
            #         }
            #     }
            # }

            # lessonList contains chapter/lesson
            # chapter
            # {
            #                 "type":"chapter",
            #                 "title":"2018年下半年真题解析",
            #                 "sorted":1,
            #                 "chapter_id":35758,
            #                 "weight":"一",
            #                 "lesson_num":"4",
            #                 "video_duration":"40分钟",
            #                 "url":"https://edu.51cto.com/center/course/lesson/index?id=",
            #                 "study_status":0,
            #                 "htime":1
            #             },
            # lesson
            #             {
            #                 "title":"2018年下半年真题解析（一）",
            #                 "describe":"讲解了2018年下半年案例分析第一道真题。",
            #                 "chapter_id":35758,
            #                 "is_look":1,
            #                 "lesson_type":1,
            #                 "lesson_id":331267,
            #                 "sorted":1,
            #                 "video_duration":"11:21",
            #                 "type":"lesson",
            #                 "weight":"1-1",
            #                 "url":"https://edu.51cto.com/center/course/lesson/index?id=331267",
            #                 "study_status":0,
            #                 "htime":1
            #             }

            if result['data'] is not False:
                data = result['data']
                page = data['currentPage']
                page_count = data['pageCount']
                lesson_list = data['lessonList']

                for lesson in lesson_list:
                    if lesson['type'] == 'chapter':
                        chapter = lesson['type']
                        continue
                    else:
                        lesson['chapter'] = chapter
                        infos.append(lesson)

                if page == page_count:
                    break
                page += 1

            else:
                break

        self.list = infos
        return self

    def sign(self, lesson_id):
        ctx = execjs.compile(tools.get_sign_js())
        return ctx.call("sign", lesson_id)

    def get_lesson_m3u8(self, lesson_id):
        sign = self.sign(lesson_id)
        url = "https://edu.51cto.com/center/player/play/get-lesson-info?" \
              "type=course&lesson_type=course&sign=%s&lesson_id=%d" % (sign, lesson_id)

        resp = self.session.get(url).text

        try:
            arr = json.loads(resp)
        except Exception, e:
            print (e.message)
            print("下载报错")
            raise Exception("""
            获取m3u8文件报错，
            链接地址：%s
            接口返回:%s
            sign: %s
            exception message: %s
            """ % (url, resp, sign, e.message))

        dispatch = arr['dispatch']
        high = dispatch[0]
        url = high['url']

        # 10s video urls
        return self.get_video_url_by_m3u8_file(url)

    def download(self):
        course_path = tools.join_path(self.path, self.course_name)
        print course_path
        tools.check_or_make_dir(course_path)

        for lesson in self.list:
            urls = self.get_lesson_m3u8(lesson['lesson_id'])
            file_name = tools.join_path(course_path, "%s.ts" % lesson['title'])
            print file_name
            if os.path.exists(file_name):
                continue
            print "download %s" % file_name
            tools.download(file_name, urls)

    def get_video_url_by_m3u8_file(self, url):
        res = self.session.get(url).text
        return re.findall(r'https.*', res)

    def set_course_id_by_course_list(self):
        url = "https://edu.51cto.com/center/course/user/ajax-info-new?page=%d&size=5&cate_id=0"
        currentPage = 1
        flag = 1
        print "以下是您购买的课程："

        while True:
            text = self.session.get(url % currentPage).text
            data = json.loads(text)['data']
            courses = data['course']
            currentPage = data['currentPage']
            totalPage = data['totalPage']
            course_desc = {}

            for course in courses:
                course_desc[course['id']] = course['title']
                print "课程ID:%d, 课程名称:%s" % (course['id'], course['title'])

            while True:
                print
                print "请输入您要下载的课程id,输入p向上翻页,输入n继续向下翻页,默认向下翻页"
                input = raw_input("课程id：")

                if input == "n" or input == "" or input == "p":
                    if input == "p":
                        flag = -1
                    elif input == "n":
                        flag = 1
                        if currentPage == totalPage:
                            break
                    currentPage += flag
                    break

                try:
                    input = int(input)
                except ValueError:
                    print "无效的输入:", input
                else:

                    if input in course_desc:
                        self.course_id = input
                        self.course_name = course_desc[input]
                        return self
                    else:
                        if input == 0:
                            exit()
                        print "无效的课程id:", input
                        break
