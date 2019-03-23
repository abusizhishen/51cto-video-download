# encoding=utf-8
import json
from cto import Login


class Lesson(object):
    lesson_id = 0
    size = 20
    page = 1

    def __init__(self, lesson_id):
        self.lesson_id = lesson_id
        self.session = Login().login()

        pass

    def get_list(self):
        infos = []
        page = self.page

        # "lessonList":Array[7],
        #         "currentPage":4,
        #         "pageCount":4,

        while True:
            url = "https://edu.51cto.com/center/course/user/get-lesson-list?page=%d&size=%d&id=%d" % \
                  (page, self.size, self.lesson_id)
            resp = self.session.get(url)
            result = json.loads(resp.text)

            if result['data'] is not False:
                data = result['data']
                page = data['currentPage']
                page_count = data['pageCount']
                lesson_list = data['lessonList']
                infos += lesson_list

                if page == page_count:
                    break
                page += 1

            else:
                break

        return infos

