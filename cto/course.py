# coding=utf-8
from cto import Login
import json, re, os, time, random, datetime, sys, cto
reload(sys)
sys.setdefaultencoding('utf-8')


class Course(object):
    course_id = 0

    def __init__(self, course_id):
        login = Login()
        self.session = login.login()
        self.course_id = course_id

    def query_course_list(self):
        url = "https://edu.51cto.com/center/course/user/get-lesson-list?size=1000&id=" % self.course_id
        resp = self.session.get(url)

        course_list_json = json.load(resp.text)
        