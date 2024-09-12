#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 用 yield 代替线程
# actor 调度
from collections import deque


class ActorScheduler:
    def __init__(self):
        self._actors = {}           # names to actors
        self._msg_queue = deque()   # 消息队列

    def new_actor(self, name, actor):
        self._msg_queue.append((actor, None))
        self._actors[name] = actor

    def send(self, name, msg):
        """
        发送消息到 actor
        """
        actor = self._actors.get(name)
        if actor:
            self._msg_queue.append((actor, msg))

    def run(self):
        """
        运行只要有消息
        """
        while self._msg_queue:
            actor, msg = self._msg_queue.popleft()
            try:
                actor.send(msg)
            except StopIteration:
                pass


if __name__ == '__main__':
    def printer():
        while True:
            msg = yield
            print('Got:', msg)

    def counter(sched):
        while True:
            # 接收当前的计数
            n = yield
            if n == 0:
                break

            # 发送 printer 任务
            sched.send('printer', n)
            # 发送下一个 count 到 counter 任务
            sched.send('counter', n-1)


    sched = ActorScheduler()
    # 初始化 actors
    sched.new_actor('printer', printer())
    sched.new_actor('counter', counter(sched))

    # 发送初始消息到 counter
    sched.send('counter', 10000)
    sched.run()
