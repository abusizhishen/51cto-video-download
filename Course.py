# encoding=utf-8
from cto import Login, lesson


def run(ss):
    try:
        lesson.Lesson(ss).set_course_id_by_course_list().lesson_list().download()
    except KeyboardInterrupt:
        print
        print('程序退出')
        exit(0)


if __name__ == '__main__':
    run()

