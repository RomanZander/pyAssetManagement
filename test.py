# -*- coding: utf-8 -*-
'''
@summary: AssetManagement testing
@since: 2012.09.21
@version: 0.0.1
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    SAQ|data compare logic
"""
# from folderScan
MQdata = [{'name': 'test-1-mediaFile.mov', 'size': 10L}, 
          {'name': 'test-2-mediaFile.mov', 'size': 10L},
          {'name': 'test-5-mediaFile.mov', 'size': 10L}, # new found
          {'name': 'test-6-mediaFile.mov', 'size': 10L}  # new found
          ]
# from DB
SQLdata = [{'name': 'test-1-mediaFile.mov', 'size': 10L}, # same
           {'name': 'test-2-mediaFile.mov', 'size': 20L}, # changed
           {'name': 'test-3-mediaFile.mov', 'size': 10L}] # obsolete

# print "MQ data: {!r}".format(MQdata)
# print "SQL data: {!r}".format(MQdata)

def insertData(data):
    print "INSERT: {0!r}".format(data)
    pass

def updateData(data):
    print "UPDATE: {0!r}".format(data)
    pass

def deleteData(data):
    print "DELETE: {0!r}".format(data)
    pass



for mqRecord in MQdata:
    if mqRecord not in SQLdata:
        # not in DB, new or modified
        print "### newborn in:\nMQ: {!r}".format(mqRecord)

for sqlRecord in SQLdata:
    if sqlRecord not in MQdata:
        # not in scan results, odl or modified   
        print "<<< obsolete in:\nSQL: {!r}".format(sqlRecord)

pass
