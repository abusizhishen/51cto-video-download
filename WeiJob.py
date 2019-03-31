# -*- coding: utf-8 -*-
import sys
from cto.wejob import Wejob
from cto import Login


def run(ss):
    try:
        w = Wejob(ss)
        train_id = w.get_train_id_by_list()
        w.train(train_id)

    except KeyboardInterrupt:
        print
        print('程序退出')
        exit(0)


if __name__ == '__main__':
    run()
