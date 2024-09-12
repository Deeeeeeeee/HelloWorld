#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import time
import threading


class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def run(self):
        while True:
            time.sleep(self._interval)
            with self._cv:
                self._flag ^= 1 # 取反 flag 的值. 0 -> 1, 1 -> 0
                self._cv.notify_all()

    def wait_for_tick(self):
        """
        等待下一个 tick
        """
        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()


ptimer = PeriodicTimer(5)
ptimer.start()

# 两个线程 synchronize 在 timer 上
def countdown(n):
    while n > 0:
        ptimer.wait_for_tick()
        print('T-minus', n)
        n -= 1

def countup(last):
    n = 0
    while n < last:
        ptimer.wait_for_tick()
        print('Counting', n)
        n += 1

# 一个向上数，一个向下数
threading.Thread(target=countdown, args=(10,)).start()
threading.Thread(target=countup, args=(5,)).start()
