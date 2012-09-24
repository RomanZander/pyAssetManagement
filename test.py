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
    unduplicate
    insert-update list
    obsolete list
    ...SAQ|data compare logic
"""

#fake unpickled MQ message body
MQbody = {'msgFolderContext': 'D:\\dev.Git\\pyAssetManagement\\test1', 
          'msgTimestamp': 1348427664.125, 'msgMessage': 'foundFile', 'msgAppID': 'scanFolder', 
          'msgPayload': [{'size': 10L, 'name': 'test-0-mediaFile.mov', 'mtime': 1345979021.703125}, 
                         {'size': 10L, 'name': 'test-1-mediaFile.Mov', 'mtime': 1345979021.71875}, 
                         {'size': 10L, 'name': 'test-2-mediaFile.MOV', 'mtime': 1345979021.734375}, 
                         {'size': 10L, 'name': 'test-3-mediaFile.mov', 'mtime': 1345979021.75} # brand new
                         ]} 
# fake data from DB: name, size, mtime (, type = 'File') 
DBdata = [{'size': 10L, 'name': 'test-0-mediaFile.mov', 'mtime': 1345979021.703125}, #same
          {'size': 20L, 'name': 'test-1-mediaFile.Mov', 'mtime': 1345979021.71875}, # mod size
          {'size': 10L, 'name': 'test-2-mediaFile.MOV', 'mtime': 1345979041.12}, # mod time 
          {'size': 10L, 'name': 'test-5-mediaFile.mov', 'mtime': 1345979061.75} # obsolete
          ]  

# payload from MQ message body
MQdata =  MQbody['msgPayload']

# filter MQdata from full duplicates with DBdata 
newbornMQdata = [mqRecord for mqRecord in MQdata if (mqRecord not in DBdata)]
# collect namelist from MQdata
namelistMQdata = [mqRecord['name'] for mqRecord in MQdata] 
# collect obsolete from DBdata with MQdataNamesList
obsoleteDBdata = [dbRecord for dbRecord in DBdata if 
                  (dbRecord['name'] not in namelistMQdata)]  

print '\n [+] newbornMQdata:\n', newbornMQdata
print '\n [-] obsoleteDBdata:\n', obsoleteDBdata

import sys
import MySQLdb

cfgMySQLhost = 'mysql'
cfgMySQLuser = 'root'
cfgMySQLpasswd = 'root'
cfgMySQLdb = 'test'

if MQbody['msgMessage'] == 'foundFile': # process files
    ###
    print '\n [:] process files'
    # Open database connection
    # prepare a cursor object using cursor() method
    try:
        conn = MySQLdb.connect(cfgMySQLhost, 
                               cfgMySQLuser, 
                               cfgMySQLpasswd,
                               cfgMySQLdb)
    except MySQLdb.Error, e:
        ###
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)
    cursor = conn.cursor()
    # execute SQL query using execute() method.
    # Fetch a single row using fetchone() method.
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    
    ###
    print "Database version : {0!r} \nrows: {1!r}".format(data, cursor.rowcount)
    
    # close cursor and disconnect from server
    cursor.close()
    conn.commit()
    conn.close()
    
    pass
pass