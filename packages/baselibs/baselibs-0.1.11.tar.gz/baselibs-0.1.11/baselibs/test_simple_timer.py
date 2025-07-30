#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

import time
from .simple_timer import TimeCount

def test_timecount():
    ''' 单元测试 '''

    tc = TimeCount()
    tc.start()
    # ... 进行某项操作 ...
    time.sleep(2.7)
    elapsed_time  = tc.pause()
    print(f"第一段时间: {elapsed_time} ms")

    tc.resume()
    # ... 继续进行其他操作 ...
    time.sleep(3.46)
    another_elapsed_time = tc.pause()
    print(f"第二段时间: {another_elapsed_time} ms")

    tc.show_splits()
    tc.show_total()


if __name__ == '__main__':
    pass

