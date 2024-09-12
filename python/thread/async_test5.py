#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import asyncio

async def show():
    print("a")
    await show2()

async def show2():
    print("b")
    show3()


def show3():
    print("c")


if __name__ == "__main__":
    asyncio.run(show())