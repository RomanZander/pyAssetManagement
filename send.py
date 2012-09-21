# -*- coding: utf-8 -*-
import sys
import time
import pika
import cPickle

content = ' '.join(sys.argv[1:]) or "Hello World!"
timestamp = time.time()
print "{!s}: Accepted: {!r}".format(
                                    time.strftime('%H:%M:%S %Y%m%d', time.localtime(timestamp)),
                                    content
                                    )
data = {
           'msgTimestamp': timestamp,
           'msgAppID': 'send.py',
           'msgPayload': content
           }
print ' [.] data:', data 
dataPickled = cPickle.dumps(data, -1)

# add record to hosts on local dev /'localhost'
parameters = pika.ConnectionParameters(host = '10.10.11.135')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(
                      queue = 'task_queue',
                      durable = True
                      )
publishproperties = pika.BasicProperties(delivery_mode = 2) # make message persistent
channel.basic_publish(exchange = '',
                      routing_key = 'task_queue',
                      body = dataPickled,
                      properties = publishproperties
                      )
                      
print " [x] Sent %r" % (dataPickled)
connection.close()
