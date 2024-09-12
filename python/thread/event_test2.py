#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import time
from threading import Thread, Event


def countdown(n, started_evt):
    print('countdown starting')
    started_evt.set()

    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)


def main():
    # 创建一个事件
    started_evt = Event()

    # 启动线程
    print('Launching countdown')
    t = Thread(target=countdown, args=(10, started_evt), daemon=True)
    t.start()

    # 等待线程开始
    started_evt.wait()
    print('countdown is running')


if __name__ == '__main__':
    main()