# encoding=utf-8
import json
from cto import Login

class Lesson(object):
    lesson_id = 0
    def __init__(self,lesson_id):
        self.lesson_id = lesson_id
        self.session = Login().login()

        pass

    def getList(self):
        url = "https://edu.51cto.com/center/course/user/get-lesson-list?size=1000&id=%d" % self.lesson_id
        resp = self.session.get(url)

        return json.loads(resp.text)