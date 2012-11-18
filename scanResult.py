#!/usr/local/bin/python
# -*- coding: utf-8 -*- 
'''
@summary: AssetManagement scanResult
@since: 2012.09.19
@version: 0.0.13
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    - subfolders processing
    - check connection
    - unite logging/pika log
    ...process unsuccess connection to RabbitMQ
    ...process unsuccess connection to In MQ channel
    ...process unsuccess connection to Out MQ channel
"""
# ---------------------------------------------------------------------------------------------
# CHANGELOG
# ---------------------------------------------------------------------------------------------
'''
    0.0.13 +processFoundSubfolder
    0.0.11 db/table in cfg
    0.0.10 pymysql instead MySQLdb
    0.0.9 +count and insert/update frames in sequences
    0.0.8 +fix processNoSubfolder, processFoldelGone, 
        processNoFile, processFoundFile, 
        processNoSequence, processFoundSequence
    0.0.6 +prosess noSubfolder, fix folderGone 
    0.0.5 +process folderGone in DB 
    0.0.4 +process foundFile in DB 
    0.0.3 +process dipatcher
    0.0.3a + rabbitmq host
    0.0.2 +inbound processor
    0.0.1 +Initial commit
'''
import os
import sys
import logging
import time
import pika
import cPickle
import pymysql
# pymysql.install_as_MySQLdb()
#import MySQLdb

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
cfgMySQLdb = 'modxTest'
cfgMySQLtable = 'am_media'

# status messages
cfgFOLDERGONE = 'folderGone'
cfgFOUNDSUBFOLDER = 'foundSubfolder'
cfgNOSUBFOLDER = 'noSubfolder'
cfgFOUNDFILE = 'foundFile'
cfgNOFILE = 'noFile'   
cfgFOUNDSEQUENCE = 'foundSequence'
cfgNOSEQUENCE = 'noSequence'

# set pika log level
pika.log.setup(pika.log.INFO) #pika.log.setup(pika.log.ERROR)

def connectMySQLdb():
    # Open database connection
    try:
        # connection = MySQLdb.connect(cfgMySQLhost,
        connection = pymysql.connect(cfgMySQLhost,
                               cfgMySQLuser, 
                               cfgMySQLpasswd,
                               cfgMySQLdb,
                               use_unicode=True,
                               charset='utf8'
                               )
    #except MySQLdb.Error, e:
    except pymysql.Error, e:
        ### TODO: log connection error
        ### TODO: reconnect tryout?
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
    print " [*] Inbound message:"
    if MQbody['msgMessage'] == cfgFOLDERGONE:
        # call message processor for obsolete folder
        processFoldelGone(MQbody)
    elif MQbody['msgMessage'] == cfgFOUNDFILE:
        # call message processor for files
        processFoundFile(MQbody)
    elif MQbody['msgMessage'] == cfgNOFILE:
        # call message processor for obsolete files
        processNoFile(MQbody)
        
    elif MQbody['msgMessage'] == cfgFOUNDSEQUENCE:
        # call message processor for sequences
        processFoundSequence(MQbody)
        ### print ' [#] processFoundSequence(MQbody)'
        
    elif MQbody['msgMessage'] == cfgNOSEQUENCE:
        # call message processor for obsolete sequences
        processNoSequence(MQbody)
        ### print ' [#] processNoSequence(MQbody)'
    
    elif MQbody['msgMessage'] == cfgFOUNDSUBFOLDER:
        # call message processor for subfolders
        processFoundSubfolder(MQbody)
    elif MQbody['msgMessage'] == cfgNOSUBFOLDER:
        # call message processor for obsolete subfolders
        processNoSubfolder(MQbody)
    
    else:
        ###
        print " [?] something else", MQbody['msgMessage']
        print " [.] Processing inbound message..."
        time.sleep(1)
    ###
    print " [x] Done\n"
    
def processFoundSequence(MQbody):
    ###
    print " [:] Processing foundSequence message..."
    msgFolderContext = MQbody['msgFolderContext']
    # expand payload data from MQ message body
    MQdata = [] # sequences list
    for item in MQbody['msgPayload']:
        # construct compound sequence name
        itemName = u"{!s}[{!s}-{!s}]{!s}".format(item['namePrefix'],
                                         item['nameIndexStart'],
                                         item['nameIndexFinish'],
                                         item['nameExtention'])
        # count sequence frames
        itemFrames = int(item['nameIndexFinish']) - int(item['nameIndexStart']) + 1 
        # fill up sequences list element
        MQdata.append({'name': itemName,
                       'size': item['size'],
                       'mtime': item['mtime'],
                       'frames': itemFrames
                       })
    # Open database connection and prepare a cursor object
    conn = connectMySQLdb() 
    cursor = conn.cursor()
    # create select SQL query
    selectSql = u'''
    SELECT `name`, `size`, `mtime`, `frames` 
    FROM ''' + cfgMySQLtable + ''' # TODO: table name?
    WHERE  (`type` = 'Sequence') AND (`path` = %s);
    ''' 
    # fill up and execute SQL query
    cursor.execute(selectSql, (msgFolderContext,
                               ))
    ### 
    print ' [?] selectSql:', cursor.rowcount
    # fetch all results and close cursor
    rows = cursor.fetchall()
    cursor.close()
    # parse rows to data list
    DBdata =[] # list for data dictionary from db
    for row in rows:
        DBdata.append({'name': row[0],
                       'size': row[1],
                       'mtime': int(row[2]), # convert to integer
                       'frames': int(row[3]) # convert to integer
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
    ### print '\n [+] newbornMQdata:\n {!r}'.format(newbornMQdata)
    ### print '\n [-] obsoleteDBdata:\n {!r}'.format(obsoleteDBdata)
    # update/insert/delete queries here:
    # NEWBORN HERE:
    for newbornRecord in newbornMQdata:
        cursor = conn.cursor()
        # TODO: compute WTF-factor
        ### 
        print ' [^] updateSql'
        # define update SQL query
        updateSql = u'''
        INSERT INTO ''' + cfgMySQLtable + ''' # TODO: table name? 
            (`path`, `name`, `type`, `size`, `mtime`, `frames`) 
        VALUES 
            (%s, %s, 'Sequence', %s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
            `size` = VALUES(`size`), 
            `mtime` = VALUES(`mtime`),
            `updated` = NOW();
        ''' # TODO: WTF-factor in SQL
        # fill up and execute query
        cursor.execute(updateSql, (msgFolderContext, # path
                                   newbornRecord['name'], # name,
                                   newbornRecord['size'], # size,
                                   newbornRecord['mtime'], # mtime,
                                   newbornRecord['frames'] # frames
                                   )) 
        cursor.close()
    # OBSOLETE HERE:
    for obsoleteRecord in obsoleteDBdata:
        cursor = conn.cursor()
        ### 
        print ' [-] deleteSql'
        # define delete SQL query
        deleteSql = u'''
        DELETE FROM ''' + cfgMySQLtable + ''' # TODO: table name?
        WHERE (`name` = %s) 
            AND (`path` = %s);
        ''' 
        # fill up and execute query
        cursor.execute(deleteSql, (obsoleteRecord['name'], # name, 
                                   msgFolderContext # path
                                   ))
        # close last cursor
        cursor.close()
    # commit and disconnect from server
    conn.commit()
    conn.close()
    
def processNoSequence(MQbody):
    ###
    print " [:] Processing noSequence message..."
    msgFolderContext = MQbody['msgFolderContext']
    # Open database connection and prepare a cursor object
    conn = connectMySQLdb() 
    cursor = conn.cursor()
    # create delete SQL query
    deleteSql = u'''
    DELETE FROM ''' + cfgMySQLtable + ''' # TODO: table name?
    WHERE 
        (`path` = %s) AND
        (`type` = 'Sequence'); 
    '''
    # fill up and execute SQL query
    cursor.execute(deleteSql, (msgFolderContext, # path
                               ))
    ### 
    print ' [-] deleteSql:', cursor.rowcount
    # close last cursor, commit and disconnect from server
    cursor.close()
    conn.commit()
    conn.close()
    
def processFoundSubfolder(MQbody):
    ###
    print " [:] Processing foundSubfolder message..."
    msgFolderContext = MQbody['msgFolderContext']
    # create subfolder mask for SQL LIKE 
    subfoldersMask = (msgFolderContext + os.sep + '%').replace('\\','\\\\')
    # expand payload from MQ message body
    MQdata = [] # sequences list
    # construct found path from subfolders list
    for item in MQbody['msgPayload']:
        itemPath = msgFolderContext + os.sep + item['name'] 
        MQdata.append(itemPath)
    # get old subfolders list:
    # open database connection and prepare a cursor object
    conn = connectMySQLdb() 
    cursor = conn.cursor()
    # create select SQL query
    selectSql = u'''
    SELECT  DISTINCT `path` 
    FROM ''' + cfgMySQLtable + ''' # TODO: table name?
    WHERE  `path` LIKE %s;
    ''' 
    # fill up and execute SQL query
    cursor.execute(selectSql, (subfoldersMask, # path
                               ))
    ### 
    print ' [?] selectSql:', cursor.rowcount
    # fetch all results and close cursor
    rows = cursor.fetchall()
    cursor.close()
    # parse rows to data list
    DBdata =[] # list for data from db
    for row in rows:
        DBdata.append(row[0]) 
    # newborn/obsolete logic here:
    # define comparison logic
    def pathBelongsTo(pathToCheck, pathList):
        belonging = False # intinal
        for pathItem in pathList:
            if pathToCheck == pathItem:
                # path is equal to current list item
                belonging = True
                break
            if pathToCheck.startswith(pathItem + os.sep):
                # path includes current list item 
                belonging = True
                break 
        return belonging
    # collect obsolete records from DBdata with MQdata
    obsoleteDBdata = [dbRecord for dbRecord in DBdata if not
                      pathBelongsTo(dbRecord, MQdata)] # belonging check
    ### print '\n [###] subfoldersMask:\n {!r}'.format(subfoldersMask)
    ### print '\n [###] MQdata:\n {!r}'.format(MQdata)
    ### print '\n [###] DBdata:\n {!r}'.format(DBdata)
    ### print '\n [###] obsoleteDBdata:\n {!r}'.format(obsoleteDBdata)
    # OBSOLETE HERE:    
    for obsoleteRecord in obsoleteDBdata:
        cursor = conn.cursor()
        # define delete SQL query
        deleteSql = u'''
        DELETE FROM ''' + cfgMySQLtable + ''' # TODO: table name?
        WHERE (`path` = %s) 
        ''' 
        # fill up and execute query
        cursor.execute(deleteSql, (obsoleteRecord, # path 
                                   ))
        ###
        print " [-] deleteSql:", cursor.rowcount
        # close last cursor
        cursor.close()
    # commit and disconnect from server
    cursor.close()
    conn.commit()
    conn.close()
    
def processNoSubfolder(MQbody):
    ###
    print " [:] Processing noSubfolder message..."
    msgFolderContext = MQbody['msgFolderContext']
    # create subfolder mask for SQL LIKE 
    subfoldersMask = (msgFolderContext + os.sep + '%').replace('\\','\\\\')
    # Open database connection and prepare a cursor object
    conn = connectMySQLdb() 
    cursor = conn.cursor()
    # create delete SQL query
    deleteSql = u'''
    DELETE FROM ''' + cfgMySQLtable + ''' # TODO: table name?
    WHERE 
        `path` LIKE %s;    
    ''' # subfolders only, i.e. '\path\to' vs '\path\to\%'
    # fill up and execute query
    cursor.execute(deleteSql, (subfoldersMask, # subfolder mask
                               ))
    print " [-] deleteSql:", cursor.rowcount
    # close last cursor, commit and disconnect from server
    cursor.close()
    conn.commit()
    conn.close()
    
def processFoldelGone(MQbody):
    ###
    print " [:] Processing folderGone message..."
    msgFolderContext = MQbody['msgFolderContext']
    #create subfolder mask for SQL LIKE 
    subfoldersMask = (msgFolderContext + os.sep + '%').replace('\\','\\\\')
    # Open database connection and prepare a cursor object
    conn = connectMySQLdb() 
    cursor = conn.cursor()
    # create delete SQL query
    deleteSql = u'''
    DELETE FROM ''' + cfgMySQLtable + ''' # TODO: table name?
    WHERE 
        (`path` = %s) OR
        (`path` LIKE %s);
    ''' # folders and subfolders, i.e. '\\path\\to' or '\\\\path\\\\to\\\\%'
    # fill up and execute SQL query
    cursor.execute(deleteSql, (msgFolderContext, # path
                               subfoldersMask # subfolder mask
                               ))
    ### 
    print ' [-] deleteSql:', cursor.rowcount
    # close last cursor, commit and disconnect from server
    cursor.close()
    conn.commit()
    conn.close()

def processNoFile(MQbody):
    ###
    print " [:] Processing noFile message..."
    msgFolderContext = MQbody['msgFolderContext']
    # Open database connection and prepare a cursor object
    conn = connectMySQLdb() 
    cursor = conn.cursor()
    # create delete SQL query
    deleteSql = u'''
    DELETE FROM ''' + cfgMySQLtable + ''' # TODO: table name?
    WHERE 
        (`path` = %s) AND
        (`type` = 'File'); 
    '''
    # fill up and execute SQL query
    cursor.execute(deleteSql, (msgFolderContext, # path
                               ))
    ### 
    print ' [-] deleteSql:', cursor.rowcount
    # close last cursor, commit and disconnect from server
    cursor.close()
    conn.commit()
    conn.close()

def processFoundFile(MQbody):
    ###
    print " [:] Processing foundFile message..."
    msgFolderContext = MQbody['msgFolderContext']
    # payload from MQ message body
    MQdata =  MQbody['msgPayload']
    # Open database connection and prepare a cursor object
    conn = connectMySQLdb() 
    cursor = conn.cursor()
    # create select SQL query
    selectSql = u'''
    SELECT `name`, `size`, `mtime` 
    FROM ''' + cfgMySQLtable + ''' # TODO: table name?
    WHERE  (`type` = 'File') AND (`path` = %s);
    ''' 
    # fill up and execute SQL query
    cursor.execute(selectSql, (msgFolderContext, # path
                               ))
    ### 
    print ' [?] selectSql:', cursor.rowcount
    # fetch all results and close cursor
    rows = cursor.fetchall()
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
    ### print '\n [+] newbornMQdata:\n {!r}'.format(newbornMQdata)
    ### print '\n [-] obsoleteDBdata:\n {!r}'.format(obsoleteDBdata)
    # update/insert/delete queries here:
    # NEWBORN HERE:
    for newbornRecord in newbornMQdata:
        cursor = conn.cursor()
        # TODO: compute WTF-factor
        ### 
        print ' [^] updateSql'
        # define update SQL query
        updateSql = u'''
        INSERT INTO ''' + cfgMySQLtable + ''' # TODO: table name? 
            (`path`, `name`, `type`, `size`, `mtime`) 
        VALUES 
            (%s, %s, 'File', %s, %s) 
        ON DUPLICATE KEY UPDATE 
            `size` = VALUES(`size`), 
            `mtime` = VALUES(`mtime`),
            `updated` = NOW();
        ''' # TODO: WTF-factor in SQL
        # fill up and execute query
        cursor.execute(updateSql, (msgFolderContext, # path 1
                                   newbornRecord['name'], # name 2,
                                   newbornRecord['size'], # size 3,
                                   newbornRecord['mtime'] # mtime 4
                                   )) 
        cursor.close()
    # OBSOLETE HERE:
    for obsoleteRecord in obsoleteDBdata:
        cursor = conn.cursor()
        ### 
        print ' [-] deleteSql'
        # define delete SQL query
        deleteSql = u'''
        DELETE FROM ''' + cfgMySQLtable + ''' # TODO: table name?
        WHERE (`name` = %s) 
            AND (`path` = %s);
        ''' 
        # fill up and execute query
        cursor.execute(deleteSql, (obsoleteRecord['name'], # name, 
                                   msgFolderContext # path
                                   ))
        cursor.close()
    # close last cursor, commit and disconnect from server
    conn.commit()
    conn.close()

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
        ### TODO: log/process unsuccess connection
        pass
