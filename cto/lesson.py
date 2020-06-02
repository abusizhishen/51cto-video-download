# encoding=utf-8
import simplejson as json, execjs, re, os
from cto import tools, decory_video


class Lesson(object):
    def __init__(self, session, path="学习"):
        self.session = session
        self.course_id = 0
        self.lesson_id = 0
        self.list = []
        self.data = []  # [['filename':'',urls:[]]]
        self.path = tools.join_path(tools.main_path(), path)
        self.sign = None
        self.size = 20
        self.page = 1
        self.course_name = ""
        self.id = None

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

    def get_sign(self, lesson_id):
        ctx = execjs.compile(tools.get_sign_js())
        return ctx.call("sign", str(lesson_id))

    def get_lesson_m3u8(self, lesson_id):
        self.sign = self.get_sign(lesson_id)
        url = "https://edu.51cto.com/center/player/play/get-lesson-info?" \
              "type=course&lesson_type=course&sign=%s&lesson_id=%d" % (self.sign, lesson_id)

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
            """ % (url, resp, self.sign, e.message))

        dispatch = arr['dispatch']
        high = dispatch[0]
        url = high['url']
        params = url.split("?")[1].split("&")
        args = {}
        for param in params:
            strs = param.split("=")
            print strs
            args[strs[0]] = strs[1]
        self.id = int(args["id"])
        # 10s video urls
        return self.get_video_url_by_m3u8_file(url)

    def download(self):
        course_path = tools.join_path(self.path, self.course_name)
        print course_path
        tools.check_or_make_dir(course_path)

        for lesson in self.list:
            lesson_id = lesson['lesson_id']

            urls = self.get_lesson_m3u8(lesson_id)
            file_name = tools.join_path(course_path, "%s.ts" % lesson['title'])
            print file_name
            if os.path.exists(file_name):
                continue
            print "download %s" % file_name
            play_key = self.get_key(self.id, lesson_id)
            print "视频解密key: %s" % play_key

            def func_decode(video_data):
                return decory_video.Video().decory(play_key, str(lesson_id), video_data)

            tools.download(file_name, urls, func_decode)

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

    # 这里的id是获取m3u8链接中的id
    # https://edu.51cto.com//center/player/play/m3u8?lesson_id=318336&id=312277&dp=high&type=course&lesson_type=course&cid=3
    def get_key(self, id, lesson_id):
        # url = "https://edu.51cto.com/center/player/play/get-key?lesson_id=318333&id=312291&type=course&lesson_type
        # =course&isPreview=0&sign=ecb00b0f73f40a6b63dc899ea3c5707f"
        url_model = "https://edu.51cto.com/center/player/play/get-key?lesson_id=%s&id=%d&type=course&lesson_type" \
                    "=course&isPreview=0&sign=%s"

        sign = self.get_sign(lesson_id)
        url = url_model % (str(lesson_id), id, sign)
        print url
        print "sign:", sign
        # print ("get_key: ", url)
        key = self.session.get(url).text
        if key == "errorSign":
            raise Exception("err:%s, url: %s" % (key, url))

        return key

    def get_key_for_wejob(self, lesson_id, course_id,url=None):
        # url = "https://edu.51cto.com/center/player/play/get-key?lesson_id=318333&id=312291&type=course&lesson_type
        # =course&isPreview=0&sign=ecb00b0f73f40a6b63dc899ea3c5707f"
        url_model = "https://edu.51cto.com/center/player/play/get-key?lesson_id=%s&id=%d&type=wejoboutcourse&lesson_type=course&isPreview=0&sign=%s"

        sign = self.get_sign(lesson_id)
        #url = url_model % (str(lesson_id), course_id, sign)
        url += "&sign=%s" % sign
        #print url
        print "sign:", sign
        # print ("get_key: ", url)
        key = self.session.get(url).text
        if key == "errorSign":
            raise Exception("err:%s, url: %s" % (key, url))

        return key

