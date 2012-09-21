# -*- coding: utf-8 -*-

# --------------------
# TODO: time\localtime?
# --------------------

import time
import pika
import cPickle

# add record to hosts on local dev /'localhost'
parameters = pika.ConnectionParameters(host = '10.10.11.135')  

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue = 'task_queue', 
                      durable = True)

print ' [*] Waiting for messages. To exit press CTRL+C\n'

def callback(ch, method, properties, body):
    print "{!s}: Received  {!r}".format(time.strftime('%H:%M:%S %Y%m%d'), body)
    data = cPickle.loads(body)
    print " [+] Unpickled {!r}".format(data)
    print " [:] {!r} : msgTimestamp\n [:] {!r} : msgAppID".format(
                             time.strftime(
                                           '%H:%M:%S %Y%m%d', 
                                           time.localtime(data['msgTimestamp'])
                                           ),
                             data['msgAppID']
                             )
    print " [.] Processing..."
    time.sleep(body.count('.'))
    print " [x] Done\n"
    
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue = 'task_queue'
                      )

channel.start_consuming()
