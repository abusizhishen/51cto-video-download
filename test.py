# encoding=utf-8
from cto import Login, lesson
import execjs

if __name__ == '__main__':
    ss = Login().login()
    lesson.Lesson(ss, 6089).lesson_list().show_all_m3u8()


