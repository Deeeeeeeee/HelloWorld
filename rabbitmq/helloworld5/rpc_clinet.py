#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# rpc 客户端
# https://www.rabbitmq.com/tutorials/tutorial-six-python
import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # 匿名的临时队列
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        # 消费指定correlation_id的消息
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    # 指定 correlation_id
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # 带上 correlation_id 参数
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))

        # 阻塞等待 response
        while self.response is None:
            print("Waiting...")
            self.connection.process_data_events(time_limit=None)

        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

# 可以复用临时队列，不是每次请求都一个新的队列
print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(f" [.] Got {response}")
response = fibonacci_rpc.call(10)
print(f" [.] Got {response}")