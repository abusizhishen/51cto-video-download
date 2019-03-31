# -*- coding: utf-8 -*-
import WeiJob,Course
from cto import Login
download_type = {
    1: {"name": "微职位", "fun": WeiJob.run},
    2: {"name": "课程",   "fun": Course.run},
}

if __name__ == '__main__':
    try:
        ss = Login().login()
        fun = lambda x: x
        while True:
            print "请选择课程类型:"
            for i in download_type:
                print "%d:%s" % (i, download_type[i]['name'])

            print
            print "输入0退出"
            input = raw_input("请选择:")

            try:
                input = int(input)
            except ValueError:
                print "无效的输入:", input
            else:
                if input in download_type:
                    fun = download_type[input]['fun']
                    break
                else:
                    if input == 0:
                        exit(0)
                    print "无效的选择:", input
        fun(ss)
    except KeyboardInterrupt:
        print
        print('程序退出')
        exit(0)

