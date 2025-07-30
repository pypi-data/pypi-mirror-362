#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

import time

class TimeCount():
    '''简单计时器'''

    def __init__(self):
        self.clean()

    def clean(self):
        '''重置计时器'''
        self.total_time = 0
        self.time_list = []
        self.split_times = []
        self.current_split_start = None
        self.status = 0

    def stop(self):
        '''停止计时器并重置'''
        self.clean()

    def restart(self):
        self.pause()
        self.resume()

    def start(self):
        self.resume()

    def begin(self, show=0):
        '''开始或继续计时'''
        if self.status == 0:
            self.current_split_start = time.time()
        else:
            self.resume()
        self.status = 1
        if show:
            print('计时开始...')

    def pause(self, pause=1):
        '''暂停计时，记录当前分段时间'''
        if self.status == 1:
            current_time = time.time()
            split_time = current_time - self.current_split_start

            self.time_list.append((self.current_split_start, current_time))
            self.split_times.append(split_time)
            self.total_time += split_time
            if pause==1:
                self.status = 0
            return split_time  # 返回毫秒数
            #* 1000, split_time * 1000 / 1000  # ms 和 s 单位
        else:
            return 0
    def resume(self):
        '''恢复计时'''
        if self.status == 0:
            self.begin(show=False)

    def show_splits(self, pre_text='用时', unit='ms'):
        '''显示所有分段时间'''
        for i, split in enumerate(self.split_times):
            if unit == 'ms':
                outtxt = f'{pre_text} 第{i + 1}段: {split * 1000:.3f} [毫秒]'
            elif unit == 's':
                outtxt = f'{pre_text} 第{i + 1}段: {split:.3f} [秒]'
            print(outtxt)

    def show(self, pre_text='总用时:', unit='ms', showmsg=1):
        ret = self.show_total(pre_text=pre_text, unit=unit, showmsg=showmsg)
        return ret

    def show_total(self, pre_text='总用时:', unit='ms', showmsg=1):
        '''显示总计时'''
        last_times = self.pause(pause=0)
        last_times_ms = last_times * 1000

        total_time_ms = self.total_time * 1000
        total_time_s = self.total_time

        if unit == 'ms':
            outtxt = f'{pre_text} {total_time_ms:.3f} [{last_times_ms:.3f}]毫秒'
            last_times = last_times_ms
        elif unit == 's':
            outtxt = f'{pre_text} {total_time_s:.3f} [{last_times:.3f}]秒'
        if showmsg==1:
            print(outtxt)
        # 依次返回：总用时毫秒数；最后用时秒数；文本
        return total_time_ms, last_times, outtxt

if __name__ == '__main__':
    pass
    test_timecount()
