# -*- coding: utf-8 -*- 
'''
@summary: AssetManagement scanResult
@since: 2012.09.19
@version: 0.0.2
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    process unsuccess connection to RabbitMQ
    process unsuccess connection to In MQ channel
    process unsuccess connection to Out MQ channel
     ...
"""
# ---------------------------------------------------------------------------------------------
# CHANGELOG
# ---------------------------------------------------------------------------------------------
'''
    0.0.2 +inbound processor
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
cfgRabbitInQueue = 'scanResult_queue'
cfgRabbitInRoutingKey = 'scanResult_queue'
cfgRabbitOutQueue = 'scanFolder_queue'
cfgRabbitOutRoutingKey = 'scanFolder_queue'

pika.log.setup(pika.log.INFO)

def inCallback(channel, method_frame, header_frame, body):
    # unpickle inbound
    data = cPickle.loads(body)
    ### logged
    pika.log.info(
                "Basic.Deliver %s delivery-tag %i: %s",
                header_frame.content_type,
                method_frame.delivery_tag,
                data)
    # call data processor
    processIn(data) 
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
def processIn(data): # process inbound message
    
    ###
    print " [.] Processing inbound message..."
    time.sleep(3)
    print " [x] Done\n"
    ###
    pass

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
                              queue = cfgRabbitInQueue,
                              durable = True)
        # set qos
        channel.basic_qos(prefetch_count=1)
        # start In consuming
        channel.basic_consume(
                              inCallback,
                              queue = cfgRabbitInQueue)
        channel.start_consuming()
        
        ###
        print "### consuming started"
        pass
    else:
        ### log unsuccess connection
        pass
