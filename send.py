# -*- coding: utf-8 -*-
import sys
import pika
import cPickle

# message = ' '.join(sys.argv[1:]) or "Hello World!"
message = [1,2,3]
print 'message:', message 
messagePickled = cPickle.dumps(message, -1)

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
                      body = messagePickled,
                      properties = publishproperties
                      )
                      
print " [x] Sent %r" % (messagePickled,)
connection.close()
