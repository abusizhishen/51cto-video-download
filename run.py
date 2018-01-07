# -*- coding: utf-8 -*-
import sys
from cto.wejob import Wejob
from cto import login

def go():
    args = sys.argv

    if len(args) < 2:
        train_id = raw_input('请输入train_id:')
    else:
        train_id = args[1]
    try:
        obj = Wejob(int(train_id))
        obj.train()
    except KeyboardInterrupt:
        print('程序退出')
        exit()

go()

