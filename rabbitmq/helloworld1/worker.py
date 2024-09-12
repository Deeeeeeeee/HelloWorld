#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# https://www.rabbitmq.com/tutorials/tutorial-two-python
# 持久化，主动ack，公平分发
import os
import sys
import pika
import time

def worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        # 主动ACK
        ch.basic_ack(delivery_tag=method.delivery_tag)


    # 公平分发。谁空闲，则发给谁
    channel.basic_qos(prefetch_count=1)
    # 不使用auto_ack
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()


if __name__ == "__main__":
    try:
        worker()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)