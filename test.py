# -*- coding: utf-8 -*-
'''
@summary: AssetManagement testing
@since: 2012.09.21
@version: 0.0.2a
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    unduplicate
    insert-update list
    obsolete list
    ...SAQ|data compare logic
"""

#fake unpickled MQ message body
MQbody = {'msgFolderContext': 'D:\\dev.Git\\pyAssetManagement\\test1', 
          'msgTimestamp': 1348427664.125, 'msgMessage': 'foundFile', 'msgAppID': 'scanFolder', 
          'msgPayload': [{'size': 10L, 'name': 'test-0-mediaFile.mov', 'mtime': 1345979021}, 
                         {'size': 10L, 'name': 'test-1-mediaFile.Mov', 'mtime': 1345979021}, 
                         {'size': 10L, 'name': 'test-2-mediaFile.MOV', 'mtime': 1345979021}, 
                         {'size': 10L, 'name': 'test-3-mediaFile.mov', 'mtime': 1345979021} # brand new
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
    # prepare a cursor object using cursor() method
    try:
        connection = MySQLdb.connect(cfgMySQLhost, 
                               cfgMySQLuser, 
                               cfgMySQLpasswd,
                               cfgMySQLdb)
    except MySQLdb.Error, e:
        ### TODO: log error
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)
    return connection 

if MQbody['msgMessage'] == 'foundFile': # process files

    ###
    print '\n [:] process files'
    
    # Open database connection and prepare a cursor object
    conn = connectMySQLdb() 
    cursor = conn.cursor()
    # execute SQL query (only `type` = 'File'
    sql = '''
    SELECT `name`, `size`, `mtime` 
    FROM `{0!s}`.`media`
    WHERE  (`type` = 'File') AND (`path` = {1!r}) # backslashes?
    # LIMIT 100
    ;
    '''
    sql = sql.format(cfgMySQLdb, MQbody['msgFolderContext']) # from fake MQ data
    ###
    print sql
    
    cursor.execute(sql)
    ###
    print "Rows: {!r}\n".format(cursor.rowcount)
    
    # Fetch 
    rows = cursor.fetchall()
    ###
    print "rows content: {!r}\n".format(rows)
    
    DBdata =[]
    for row in rows:
        DBdata.append({'name': row[0],
                       'size': row[1],
                       'mtime': int(row[2])
                       })
    # close cursor and disconnect from server
    cursor.close()
    conn.commit()
    conn.close()
    
    ###
    print "MQdata: {!r}\n".format(MQdata)
    ###
    print "DBdata: {!r}\n".format(DBdata)

    
    # -----------------------------------------------------------
    
    '''
    # fake data from DB: name, size, mtime (, type = 'File') 
    DBdata = [{'size': 10L, 'name': 'test-0-mediaFile.mov', 'mtime': 1345979021}, #same
              {'size': 20L, 'name': 'test-1-mediaFile.Mov', 'mtime': 1345979021}, # mod size
              {'size': 10L, 'name': 'test-2-mediaFile.MOV', 'mtime': 1345979041}, # mod time 
              {'size': 10L, 'name': 'test-5-mediaFile.mov', 'mtime': 1345979061} # obsolete
              ]  
    '''
    
    # filter MQdata from full duplicates with DBdata 
    newbornMQdata = [mqRecord for mqRecord in MQdata if (mqRecord not in DBdata)]
    # collect namelist from MQdata
    namelistMQdata = [mqRecord['name'] for mqRecord in MQdata] 
    # collect obsolete from DBdata with MQdataNamesList
    obsoleteDBdata = [dbRecord for dbRecord in DBdata if 
                      (dbRecord['name'] not in namelistMQdata)]  
    
    print '\n [+] newbornMQdata:\n {!r}'.format(newbornMQdata)
    print '\n [-] obsoleteDBdata:\n {!r}'.format(obsoleteDBdata)
    
    
    
    
    
    pass
pass