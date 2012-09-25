# -*- coding: utf-8 -*- 
'''
@summary: AssetManagement scanResult
@since: 2012.09.19
@version: 0.0.4
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
    0.0.4 +process foundFile in DB 
    0.0.3 +process dipatcher
    0.0.3a + rabbitmq host
    0.0.2 +inbound processor
    0.0.1 +Initial commit
'''
import sys
import logging
import time
import pika
import cPickle
import MySQLdb

# config for RabbitMQ
cfgRabbitAppID = 'scanResult' # script identificator
cfgRabbitHost = 'rabbitmq' # add record to hosts on local dev
cfgRabbitExchange = ''
cfgRabbitInQueue = 'scanResult_queue'
cfgRabbitInRoutingKey = 'scanResult_queue'
cfgRabbitOutQueue = 'scanFolder_queue'
cfgRabbitOutRoutingKey = 'scanFolder_queue'
# config for MySQL
cfgMySQLhost = 'mysql'
cfgMySQLuser = 'root'
cfgMySQLpasswd = 'root'
cfgMySQLdb = 'test'

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

def connectMySQLdb():
    # Open database connection
    try:
        connection = MySQLdb.connect(cfgMySQLhost, 
                               cfgMySQLuser, 
                               cfgMySQLpasswd,
                               cfgMySQLdb)
    except MySQLdb.Error, e:
        ### TODO: log connection error
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)
    return connection

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
    if MQbody['msgMessage'] == cfgFOUNDFILE:
        # call message processor
        processFoundFile(MQbody)
    else:
        ###
        print " [?] some else", MQbody['msgMessage']
        print " [.] Processing inbound message..."
        time.sleep(3)
    ###
    print " [x] Done\n"

def processFoundFile(MQbody):
    ###
    print " [:] Processing foundFile message..."
    msgFolderContext = MQbody['msgFolderContext']
    # payload from MQ message body
    MQdata =  MQbody['msgPayload']
    # Open database connection and prepare a cursor object
    conn = connectMySQLdb() 
    cursor = conn.cursor()
    # create and fill up SQL query
    selectSql = '''
    SELECT `name`, `size`, `mtime` 
    FROM `{0!s}`.`media`
    WHERE  (`type` = 'File') AND (`path` = {1!r}); # TODO: backslashes?
    '''
    selectSql = selectSql.format(cfgMySQLdb, # table, path
                                 msgFolderContext) 
    ### print selectSql
    print ' [?] selectSql'
    # execute SQL query and fetch all results
    cursor.execute(selectSql)
    rows = cursor.fetchall()
    ### print "Rows: {!r}\nrows content: {!r}\n".format(cursor.rowcount, rows)
    cursor.close()
    # parse rows to data list
    DBdata =[] # list for data dictionary from db
    for row in rows:
        DBdata.append({'name': row[0],
                       'size': row[1],
                       'mtime': int(row[2]) # convert to integer
                       })
    # newborn/obsolete logic here:
    # filter MQdata from full duplicates with DBdata 
    newbornMQdata = [mqRecord for mqRecord in MQdata if 
                     (mqRecord not in DBdata)]
    # collect namelist from MQdata
    namelistMQdata = [mqRecord['name'] for mqRecord in MQdata] 
    # collect obsolete from DBdata with MQdataNamesList
    obsoleteDBdata = [dbRecord for dbRecord in DBdata if 
                      (dbRecord['name'] not in namelistMQdata)]  
    # update/insert/delete queries here:
    for newbornRecord in newbornMQdata:
        cursor = conn.cursor()
        updateSql = '''
        INSERT INTO `{0!s}`.`media` 
            (`path`, `name`, `type`, `size`, `mtime`) 
        VALUES 
            ({1!r}, {2!r}, 'File', {3!s}, {4!s}) 
        ON DUPLICATE KEY UPDATE 
            `size` = VALUES(`size`), 
            `mtime` = VALUES(`mtime`),
            `updated` = NOW();
        '''
        updateSql = updateSql.format(cfgMySQLdb, # table 0,
                                     msgFolderContext, # path 1
                                     newbornRecord['name'], # name 2,
                                     newbornRecord['size'], # size 3,
                                     newbornRecord['mtime']) # mtime 4, 
        ### print updateSql
        print ' [^] updateSql'
        cursor.execute(updateSql)
        cursor.close()
    # delete queries here:
    for obsoleteRecord in obsoleteDBdata:
        cursor = conn.cursor()
        deleteSql = '''
        DELETE FROM `{0!s}`.`media` 
        WHERE (`media`.`name` = '{1!s}') 
            AND (`media`.`path` = {2!r}); # TODO: backslashes?
        '''
        deleteSql = deleteSql.format(cfgMySQLdb, # table, 
                                     obsoleteRecord['name'], # name, 
                                     msgFolderContext) # path
        ### print deleteSql
        print ' [-] deleteSql'
        cursor.execute(deleteSql)
        cursor.close()
    # close last cursor, commit and disconnect from server
    conn.commit()
    conn.close()
    ### print '\n [+] newbornMQdata:\n {!r}'.format(newbornMQdata)
    ### print '\n [-] obsoleteDBdata:\n {!r}'.format(obsoleteDBdata)

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
