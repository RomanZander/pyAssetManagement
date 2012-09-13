# -*- coding: utf-8 -*-
import time
import pika

parameters = pika.ConnectionParameters(host = 'localhost')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue = 'task_queue', 
                      durable = True)

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [v] Received %r" % (body,)
    time.sleep(body.count('.'))
    print " [x] Done"
    
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue = 'task_queue'
                      )

channel.start_consuming()
