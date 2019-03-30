# encoding=utf-8
import simplejson as json, execjs,re
from cto import Login,tools


class Lesson(object):
    lesson_id = 0
    size = 20
    page = 1

    def __init__(self, session, course_id):
        self.session = session
        self.course_id = course_id
        self.lesson_id = 0
        self.list = []
        self.data = []  # [['filename':'',urls:[]]]
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

    def sign(self):
        f = open("./js/h5player.js")
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()

        ctx = execjs.compile(htmlstr)
        return ctx.call("sign", self.lesson_id)

    def get_lesson_m3u8(self, lesson_id):
        url = "https://edu.51cto.com/center/player/play/get-lesson-info?" \
              "type=course&lesson_type=course&sign=%s&lesson_id=%d" % (self.sign(), lesson_id)

        resp = self.session.get(url).text

        arr = json.loads(resp)
        dispatch = arr['dispatch']
        high = dispatch[0]
        url = high['url']

        # 10s video urls
        return self.get_video_url_by_m3u8_file(url)

    def show_all_m3u8(self):
        print len(self.list)
        for lesson in self.list:
            urls = self.get_lesson_m3u8(lesson['lesson_id'])

            print "download %s" % lesson['title']
            tools.download("video/"+lesson['title']+".ts", urls)

    def get_video_url_by_m3u8_file(self, url):
        res = self.session.get(url).text
        return re.findall(r'https.*', res)

    def down(self):
        self.lesson_list().show_all_m3u8()

