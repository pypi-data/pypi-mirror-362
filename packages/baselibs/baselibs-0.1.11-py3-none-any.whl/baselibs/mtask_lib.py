#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

'''
多进程管理器，可控制正在运行的最大进程数量。
只有进程完成后，才会添加新的进程。
一般情况下，最大进程数量与CPU内核个数相同

使用方法：
初始化时，使用max_process设定最大进程数量；
然后使用 wait_add 添加进程；
'''

import multiprocessing as mp
import time

class MutliTask(object):
    ''' 多进程管理器
    '''
    def __init__(self, max_process=4):
        # 最大进程数量，一般跟CPU内核个数相同
        self.max_process = max_process
        self.process_list = []
        self.debug = 0
        self.interval = 1 # 检测时间：秒

    def wait_add(self, fun, args):
        ''' 等待空闲时添加任务
        '''
        while 1:
            # 清除完成的进程
            for p in self.process_list:
                is_alive = p.is_alive()
                if not is_alive:
                    self.process_list.remove(p)

            # 判断进程总数
            total = len(self.process_list)
            if total < self.max_process: break;
            if self.debug:
                pid_list = ','.join([f"{x.pid}" for x in self.process_list])
                print(f'\r当前进程:{pid_list}', end='', flush=True)
            # 每隔几秒检测一下
            time.sleep(self.interval)

        # 创建新进程
        process = mp.Process(target=fun, args=args)
        self.process_list.append(process)
        process.start()
        pid = process.pid
        if self.debug:
            print('新进程:', process.pid)
        return pid

    def wait_finished(self):
        ''' 等待全部任务都完成
        '''
        while 1:
            # 清除完成的进程
            try:
                for p in self.process_list:
                    is_alive = p.is_alive()
                    if not is_alive:
                        self.process_list.remove(p)
            except Exception as e:
                pass

            # 判断进程总数
            total = len(self.process_list)
            if total == 0: break;

    def __kill__(self):
        ''' 删除
        '''
        try:
            # return
            for p in self.process_list:
                p.terminate()
        except Exception as e:
            pass


if __name__ == '__main__':
    pass
