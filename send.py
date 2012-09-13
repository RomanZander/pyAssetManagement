# -*- coding: utf-8 -*-
import sys
import pika

message = ' '.join(sys.argv[1:]) or "Hello World!"

parameters = pika.ConnectionParameters(host = 'localhost')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(
                      queue = 'task_queue',
                      durable = True
                      )
publishproperties = pika.BasicProperties(delivery_mode = 2) # make message persistent
channel.basic_publish(exchange = '',
                      routing_key = 'task_queue',
                      body = message,
                      properties = publishproperties
                      )
                      
print " [x] Sent %r" % (message,)
connection.close()
