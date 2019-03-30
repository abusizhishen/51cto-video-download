# -*- coding: utf-8 -*-
import sys
from cto.wejob import Wejob
from cto import Login


if __name__ == '__main__':
    try:
        session = Login().login()
        w = Wejob(session)
        train_id = w.get_train_id_by_list()
        w.train(train_id)

    except KeyboardInterrupt:
        print
        print('程序退出')
        exit(0)