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
# from FolderScan
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

for mqRecord in MQdata:
    if mqRecord in SQLdata:
        # same record
        print "=== same records:\nMQ: {!r}".format(mqRecord)
    else:
        print "### new in:\nMQ: {!r}".format(mqRecord)

for sqlRecord in SQLdata:
    if sqlRecord not in MQdata:
        print "<<< obsolete in:\nSQL: {!r}".format(sqlRecord)

pass
