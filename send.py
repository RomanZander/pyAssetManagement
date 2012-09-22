# -*- coding: utf-8 -*-
'''
@summary: AssetManagement send test
@since: 2012.09.13
@version: 0.0.7a
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
'''
    ...come pika.log
'''

import time
import pika
import cPickle

# config for RabbitMQ
cfgRabbitAppID = 'send test' # script identificator
cfgRabbitHost = 'rabbitmq' # 127.0.0.1 in hosts on local dev
cfgRabbitExchange = ''
# cfgRabbitInQueue = 'scanResult_queue'
# cfgRabbitInRoutingKey = 'scanResult_queue'
cfgRabbitOutQueue = 'scanResult_queue'
cfgRabbitOutRoutingKey = 'scanResult_queue'

def sendMessageToQM(message, content = None): # send message to MQ server
    # create RabbitMQ connection
    parameters = pika.ConnectionParameters(host = cfgRabbitHost)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    if connection.is_open:
        # get current timestamp
        timestamp = time.time()
        # An agreement about message:
        data = {'msgTimestamp': timestamp,
                'msgAppID': cfgRabbitAppID,
                'msgMessage': message,
                'msgPayload': content
                }
        # conserve data
        dataPickled = cPickle.dumps(data, -1)
        # MQ code here
        channel.queue_declare(
                    queue = cfgRabbitOutQueue,
                    durable = True
                    )
        publishproperties = pika.BasicProperties(
                    delivery_mode = 2 # make message persistent 
                    ) 
        channel.basic_publish(
                    exchange = cfgRabbitExchange,
                    routing_key = cfgRabbitOutRoutingKey,
                    body = dataPickled, # sent data
                    properties = publishproperties
                    )        
        # logging output
        # logging.info('send to MQ: %s | %s', message, content)
        connection.close()
    pass

pika.log.setup(pika.log.INFO) # some logging

# fake data
fakeData = [{'path': 'D:\\dev.Git\\pyAssetManagement', 
             'mtime': 1348263628.8125, 'name': '.git', 'size': 0L}, 
            {'path': 'D:\\dev.Git\\pyAssetManagement', 
             'mtime': 1346000334.859375, 'name': '.settings', 'size': 0L},
            {'path': 'D:\\dev.Git\\pyAssetManagement', 
             'mtime': 1347149587.28125, 'name': 'test1', 'size': 0L},
            {'path': 'D:\\dev.Git\\pyAssetManagement', 
             'mtime': 1347388255.8125, 'name': 'test2', 'size': 0L}]
fakeMessage = 'Subfolders found'
'''
INFO | 2012-09-22 22:06:55,121 | send to MQ: Subfolders found | [{'path': 'D:\\dev.Git\\pyAssetManagement', 'mtime': 134
8263628.8125, 'name': '.git', 'size': 0L}, {'path': 'D:\\dev.Git\\pyAssetManagement', 'mtime': 1346000334.859375, 'name'
: '.settings', 'size': 0L}, {'path': 'D:\\dev.Git\\pyAssetManagement', 'mtime': 1347149587.28125, 'name': 'test1', 'size
': 0L}, {'path': 'D:\\dev.Git\\pyAssetManagement', 'mtime': 1347388255.8125, 'name': 'test2', 'size': 0L}]
INFO | 2012-09-22 22:06:55,138 | send to MQ: NO File-media found | D:\dev.Git\pyAssetManagement
INFO | 2012-09-22 22:06:55,153 | send to MQ: NO Sequence-media found | D:\dev.Git\pyAssetManagement
'''

sendMessageToQM(fakeMessage, fakeData)
        
