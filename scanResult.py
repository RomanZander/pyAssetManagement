# -*- coding: utf-8 -*- 
'''
@summary: AssetManagement scanResult
@since: 2012.09.19
@version: 0.0.3
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    ...send new subfolder tasks to MQ
    ...SQL|data comparing logic
    ...process unsuccess connection to RabbitMQ
    ...process unsuccess connection to In MQ channel
    ...process unsuccess connection to Out MQ channel
"""
# ---------------------------------------------------------------------------------------------
# CHANGELOG
# ---------------------------------------------------------------------------------------------
'''
    0.0.3 +process dipatcher
    0.0.3a + rabbitmq host
    0.0.2 +inbound processor
    0.0.1 +Initial commit
'''
import logging
import time
import pika
import cPickle

# config for RabbitMQ
cfgRabbitAppID = 'scanResult' # script identificator
cfgRabbitHost = 'rabbitmq' # add record to hosts on local dev
cfgRabbitExchange = ''
cfgRabbitInQueue = 'scanResult_queue'
cfgRabbitInRoutingKey = 'scanResult_queue'
cfgRabbitOutQueue = 'scanFolder_queue'
cfgRabbitOutRoutingKey = 'scanFolder_queue'

# status messages
cfgFOLDERGONE = 'folderGone'
cfgFOUNDSUBFOLDER = 'foundSubfolder'
cfgNOSUBFOLDER = 'noSubfolder'
cfgFOUNDFILE = 'foundFile'
cfgNOFILE = 'noFile'   
cfgFOUNDSEQUENCE = 'foundSequence'
cfgNOSEQUENCE = 'noSequence'

# set pika log level
pika.log.setup(pika.log.INFO)
#pika.log.setup(pika.log.ERROR)

def inCallback(channel, method_frame, header_frame, body):
    # unpickle inbound
    data = cPickle.loads(body)
    # logged
    pika.log.info(
                "Basic.Deliver %s delivery-tag %i: %s",
                header_frame.content_type,
                method_frame.delivery_tag,
                data)
    # call inbound data dispatcher
    dispatchIn(data)
    # send acknowledge 
    channel.basic_ack(delivery_tag = method_frame.delivery_tag)
    pass

def dispatchIn(MQbody): # process inbound message
    ###
    print " [.] Inbound message:"
    
    msgMessage = MQbody['msgMessage']
    if msgMessage == cfgFOUNDFILE:
        ###
        print " [+] cfgFOUNDFILE", msgMessage
        
        
        
    else:
        print " [?] some else"
    
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
    channel = connection.channel() #default channel
    if connection.is_open:
        channel.queue_declare(queue = cfgRabbitInQueue,
                              durable = True)
        channel.basic_qos(prefetch_count=1) # set qos
        channel.basic_consume(inCallback, # set callback 
                              queue = cfgRabbitInQueue)
        # if logged
        pika.log.info("Connection success, consuming start, queue: %s",
                      cfgRabbitInQueue)
        channel.start_consuming() # start In consuming
        pass
    else:
        ### log unsuccess connection
        pass
