#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

from baselibs.mtask_lib import MutliTask

import time

def proc_test(x):
    for i in range(x):
        # print('%d: %d' % (x,i))
        time.sleep(0.5)
    print('工作完成！')

def test_multitask():
    ''' 单元测试
    '''
    print('最大进程：4个')
    mt = MutliTask(max_process=4)
    mt.debug = 1
    print('正在启动多个进程...')
    for i in [8, 10, 20, 35, 16, 9]:
        mt.wait_add(proc_test, (i,))

if __name__ == '__main__':
    pass

