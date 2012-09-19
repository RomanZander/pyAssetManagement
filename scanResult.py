# -*- coding: utf-8 -*- 
'''
@summary: AssetManagement scanResult
@since: 2012.09.19
@version: 0.0.1
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    ...
"""
# ---------------------------------------------------------------------------------------------
# CHANGELOG
# ---------------------------------------------------------------------------------------------
'''
    0.0.1 +Initial commit
'''
import logging
import time
import pika
import cPickle

# config for RabbitMQ
cfgRabbitAppID = 'scanResult' # script identificator
cfgRabbitHost = 'localhost'
cfgRabbitExchange = ''
cfgRabbitQueue = 'scanResult_queue'
cfgRabbitRoutingKey = 'scanResult_queue'

pika.log.setup(pika.log.INFO)

def callback(channel, method_frame, header_frame, body):
    
    data = cPickle.loads(body)
    # Receive the data in 3 frames from RabbitMQ
    pika.log.info(
                "Basic.Deliver %s delivery-tag %i: %s",
                header_frame.content_type,
                method_frame.delivery_tag,
                data)
    ###
    print " [.] Processing..."
    time.sleep(body.count('.'))
    print " [x] Done\n"
    ###
    channel.basic_ack(delivery_tag = method_frame.delivery_tag)
    pass
'''
def handle_delivery(channel, method_frame, header_frame, body):
    # Receive the data in 3 frames from RabbitMQ
    pika.log.info("Basic.Deliver %s delivery-tag %i: %s",
                  header_frame.content_type,
                  method_frame.delivery_tag,
                  body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

'''
if __name__ == '__main__':
    # create RabbitMQ connection
    parameters = pika.ConnectionParameters(host = cfgRabbitHost)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    if connection.is_open:
        ### log success
        print ' [*] Waiting for messages. To exit press CTRL+C\n'
        # MQ code here
        channel.queue_declare(
                    queue = cfgRabbitQueue,
                    durable = True)
        channel.basic_qos(prefetch_count=1) # one by one
        # start consuming
        channel.basic_consume(callback,
                    queue = cfgRabbitQueue
                    )
        channel.start_consuming()
        pass
    else:
        ### log unsuccess connection
        pass
