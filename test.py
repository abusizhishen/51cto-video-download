# encoding=utf-8
from cto import Login,lesson

if __name__ == '__main__':
    infos = lesson.Lesson(11058).get_list()

    print len(infos)
    for i in infos:
        print len(i), i
    pass

