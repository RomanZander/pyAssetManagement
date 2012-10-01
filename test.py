# -*- coding: utf-8 -*-
'''
@summary: AssetManagement testing
@since: 2012.09.21
@version: 0.0.3
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    ...rertieve in unicode
"""

# ------------------------------------------------------------------
# MySQL test
# ------------------------------------------------------------------

import sys
import os
import MySQLdb

"""
print "os.name: {!s}".format(os.name)
print "sys.getfilesystemencoding(): {!s}".format(sys.getfilesystemencoding())
print "sys.getdefaultencoding(): {!s}".format(sys.getdefaultencoding())
print "sys.stdin.encoding: {!s}".format(sys.stdin.encoding)
"""

# config for MySQL
cfgMySQLhost = 'mysql'
cfgMySQLuser = 'root'
cfgMySQLpasswd = 'root'
cfgMySQLdb = 'test'

# define console encoding
# TODO: test on other systems
if os.name == 'nt':
    cfgConsoleEnc = 'cp1251' # for arg taked from console under Window
if os.name == 'posix':
    cfgConsoleEnc = 'utf8' # for console under etc...

def connectMySQLdb():
    # Open database connection
    try:
        connection = MySQLdb.connect(cfgMySQLhost, 
                               cfgMySQLuser, 
                               cfgMySQLpasswd,
                               cfgMySQLdb,
                               charset='utf8'
                               )
    except MySQLdb.Error, e:
        ### TODO: log connection error
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)
    return connection 

cfgScanRoot = u"test1"

# encode arg from console
if len(sys.argv) >1:
    cfgScanRoot = unicode(sys.argv[1], cfgConsoleEnc) # encode from console
# real path reconstruction
cfgScanRoot = os.path.realpath(cfgScanRoot) 
print "after:", cfgScanRoot, type(cfgScanRoot)

rawDirList = os.listdir(cfgScanRoot)
print "os.listdir: "
for name in rawDirList:
    print u"{!r}".format(name)
    pass
#for name in rawDirList:
#    print name

# Open database connection and prepare a cursor object
conn = connectMySQLdb() 
cursor = conn.cursor()
sql = u'''
    INSERT INTO `test`.`media` 
            (`path`, `name`, `type`, `size`, `mtime`) 
        VALUES 
            (%s, %s, 'File', %s, %s) 
        ON DUPLICATE KEY UPDATE 
            `size` = VALUES(`size`), 
            `mtime` = VALUES(`mtime`),
            `updated` = NOW();
    '''
for name in rawDirList:
    cursor.execute(sql,
                   (#cfgMySQLdb, #table
                    cfgScanRoot,# path
                    name, # name
                    100L, # size
                    123456789 # mtime
                    ))
    rows = cursor.fetchall()
cursor.close()
conn.commit()
conn.close()
exit()
