#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Stream 只能添加日志，可以重复读，直到过期
# https://www.rabbitmq.com/tutorials/tutorial-one-python-stream
import asyncio
from rstream import Producer


STREAM_NAME = "hello-python-stream"
# 5GB
STREAM_RETENTION = 5000000000


async def send():
    async with Producer(
            host="localhost",
            username="guest",
            password="guest"
        ) as producer:
        # 幂等声明，只有不存在才会创建. 保留5GB的策略
        await producer.create_stream(
            STREAM_NAME,
            exists_ok=True,
            arguments={"max-length-bytes": STREAM_RETENTION}
        )
        # 发消息
        await producer.send(stream=STREAM_NAME, message=b"Hello world!")

        print(" [x] Hello, World! message sent")
        input(" [x] Press Enter to close the producer  ...")


with asyncio.Runner() as runner:
    runner.run(send())