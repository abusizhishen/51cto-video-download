# -*- coding: utf-8 -*-
import sys
from cto.wejob import Wejob

def go():
    args = sys.argv

    if len(args) < 2:
        train_id = raw_input('请输入train_id:')
    else:
        train_id = args[1]
    try:
        Wejob(int(train_id)).train()
    except KeyboardInterrupt:
        print('程序退出')
        exit()

go()

