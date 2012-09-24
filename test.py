# -*- coding: utf-8 -*-
'''
@summary: AssetManagement testing
@since: 2012.09.21
@version: 0.0.2
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    ...logging
    ...exceptions process
"""

#fake unpickled MQ message body
MQbody = {'msgFolderContext': 'D:\\dev.Git\\pyAssetManagement\\test2', 
          'msgTimestamp': 1348427664.125, 'msgMessage': 'foundFile', 'msgAppID': 'scanFolder', 
          'msgPayload': [{'size': 3L, 'name': 'test-0-mediaFile.mov', 'mtime': 1345979090}, 
                         {'size': 3L, 'name': 'test-1-mediaFile.mov', 'mtime': 1345979090}, 
                         {'size': 3L, 'name': 'test-12-mediaFile.MOV', 'mtime': 1345979090}, 
                         {'size': 5L, 'name': 'test-13-mediaFile.mov', 'mtime': 1345979090}
                         ]} 
# payload from MQ message body
MQdata =  MQbody['msgPayload']

# ------------------------------------------------------------------
# MySQL test
# ------------------------------------------------------------------

import sys
import MySQLdb

cfgMySQLhost = 'mysql'
cfgMySQLuser = 'root'
cfgMySQLpasswd = 'root'
cfgMySQLdb = 'test'

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

if MQbody['msgMessage'] == 'foundFile': # process files

    ###
    print '\n [:] process files'
    
    msgFolderContext = MQbody['msgFolderContext']
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
                                     newbornRecord['mtime'], # mtime 4, 
                                     )
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
    
    
    
    
    pass
pass