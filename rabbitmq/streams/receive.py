#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Stream 只能添加日志，可以重复读，直到过期
# https://www.rabbitmq.com/tutorials/tutorial-one-python-stream
import asyncio
import signal
from rstream import (
    AMQPMessage,
    Consumer,
    MessageContext,
    ConsumerOffsetSpecification,
    OffsetType
)


STREAM_NAME = "hello-python-stream"
# 5GB
STREAM_RETENTION = 5000000000


async def receive():
    consumer = Consumer(host="localhost", username="guest", password="guest")
    # 幂等声明，不存在才创建
    await consumer.create_stream(
        STREAM_NAME,
        exists_ok=True,
        arguments={"max-length-bytes": STREAM_RETENTION}
    )

    # 回调函数
    async def on_message(msg: AMQPMessage, message_context: MessageContext):
        stream = message_context.consumer.get_stream(message_context.subscriber_name)
        print("Got message: {} from stream: {}".format(msg, stream))

    # offset_specification 定义了消费者的起始点. 这里是最开始的点
    await consumer.start()
    await consumer.subscribe(
        stream=STREAM_NAME,
        callback=on_message,
        offset_specification=ConsumerOffsetSpecification(OffsetType.FIRST, None)
    )

    try:
        await consumer.run()
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("Closing Consumer...")
        return


with asyncio.Runner() as runner:
    runner.run(receive())