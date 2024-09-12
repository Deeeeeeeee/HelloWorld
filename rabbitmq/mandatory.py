#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# mandatory 参数，没有路由到队列，会返回给生产者
# 但只设置 mandatory，不使用 confirm_delivery，会不确定 return 消息的时间
# 如果消息 reject，没有效果
# 详见 basic_publish 的注释
import os
import sys
import pika
import time

import pika.adapters.blocking_connection
import pika.exceptions


def new_task():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='mandatory_ex', exchange_type='direct')

    # confirm 模式
    channel.confirm_delivery()

    # 即使 reject 了，这里也没有回调。需要测试被 broker 拒绝的情况
    def callback(ch, method, properties, body):
        print(" [x] Rejected by Broker %r" % body)
    channel.add_on_return_callback(callback)

    # 用 mandatory 参数
    try:
        channel.basic_publish(exchange='mandatory_ex', routing_key='mandatory_not_exist',
                              body='hello world', mandatory=True)
        print(' [x] Sent "hello world"')
    # 没路由到队列
    except pika.exceptions.UnroutableError as e:
        assert isinstance(e.messages, pika.adapters.blocking_connection.ReturnedMessage)
        return_messages = e.messages
        print(' [x] UnroutableError')
    # 被 broker 拒绝了
    except pika.exceptions.NackError as e:
        assert isinstance(e.messages, pika.adapters.blocking_connection.ReturnedMessage)
        return_messages = e.messages
        print(' [x] NackError')

    time.sleep(2)
    connection.close()


def worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 创建 exchange
    channel.exchange_declare(exchange='mandatory_ex', exchange_type='direct')

    # 创建队列
    channel.queue_declare(queue='mandatory_queue', durable=True)

    # 绑定 exchange 和 queue
    channel.queue_bind(exchange='mandatory_ex', queue='mandatory_queue')

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Reject %r" % body)
        # requeue 为 False 会丢失消息，True 会让 broker 重新发送消息
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
    # 这里不用 auto_ack
    channel.basic_consume(queue='mandatory_queue', on_message_callback=callback, auto_ack=False)

    channel.start_consuming()


if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        if args[0] == 'worker':
            worker()
        elif args[0] == 'new_task':
            new_task()
        else:
            print('Usage: %s worker|new_task' % sys.argv[0])
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)