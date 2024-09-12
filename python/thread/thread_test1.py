#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import time
import threading


class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(5)


def new_thread_task():
    c = CountdownTask()

    t = threading.Thread(target=c.run, args=(10,), daemon=True)
    t.start()

    c.terminate() # 线程信号
    t.join() # 等待线程结束


if __name__ == '__main__':
    new_thread_task()