#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from queue import Queue
from threading import Thread

# 用来通知结束的对象
_sentinel = object()


from concurrent.futures import ProcessPoolExecutor

import threading
from threading import RLock, Lock

lock1 = Lock()
lock2 = Lock()


def run1():
    lock1.acquire()
    print(threading.current_thread())
    lock2.acquire()
    print(threading.current_thread())
    lock2.release()
    print(threading.current_thread())
    lock1.release()

def run2():
    lock2.acquire()
    print(threading.current_thread())
    lock1.acquire()
    print(threading.current_thread())
    lock1.release()
    print(threading.current_thread())
    lock2.release()


t1 = Thread(target=run1, daemon=True)
t2 = Thread(target=run2, daemon=True)

t1.start()
t2.start()

t1.join()
t2.join()