#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

def generator():
    print('a')
    while True:
        b = yield
        print(b)

f = generator()
data = f.send(None)
# print(data)
data = f.send(10)
# print(data)
data = f.send(20)
# print(data)