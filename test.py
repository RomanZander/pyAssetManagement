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
    ...listdir in unicode
    ...store in unicode
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


###

cfgScanRoot = u"test5\тест"

# encode arg from console    
if len(sys.argv) >1:
    cfgScanRoot = unicode(sys.argv[1], cfgConsoleEnc) # encode from console
# real path reconstruction
cfgScanRoot = os.path.realpath(cfgScanRoot) 
print "after:", cfgScanRoot, type(cfgScanRoot)

rawDirList = os.listdir(cfgScanRoot)
print "os.listdir: ", rawDirList
#for name in rawDirList:
#    print name

# Open database connection and prepare a cursor object
conn = connectMySQLdb() 
cursor = conn.cursor()

updateSql = u'''
    INSERT INTO `{0!s}`.`media` 
            (`path`, `name`, `type`, `size`, `mtime`) 
        VALUES 
            ('{1!s}', '{2!s}', 'File', {3!s}, {4!s}) 
        ON DUPLICATE KEY UPDATE 
            `size` = VALUES(`size`), 
            `mtime` = VALUES(`mtime`),
            `updated` = NOW();
    '''

for name in range(1, 5): #rawDirList:
    sql = updateSql.format(cfgMySQLdb, #table
                           MySQLdb.escape_string(unicode(cfgScanRoot,'utf-8')),# path 
                           name, # name
                           100L, # size
                           123456789 # mtime
                           )
    print sql
    cursor.execute(sql)
    rows = cursor.fetchall()
    print "Rows: {!r}\nrows content: {!r}\n".format(cursor.rowcount, rows)


cursor.close()
conn.commit()
conn.close()
exit()



"""
# Open database connection and prepare a cursor object
conn = connectMySQLdb() 
cursor = conn.cursor()
# create and fill up SQL query
selectSql = '''
SELECT `name`, `size`, `mtime` 
FROM `{0!s}`.`media`
WHERE  (`type` = 'File') AND (`path` = {1!r}); # TODO: backslashes?
'''
#selectSql = selectSql.format(cfgMySQLdb, # table, path
#                             msgFolderContext) 
### 
print selectSql
print ' [?] selectSql'
# execute SQL query and fetch all results
cursor.execute(selectSql)
rows = cursor.fetchall()
### print "Rows: {!r}\nrows content: {!r}\n".format(cursor.rowcount, rows)
cursor.close()
conn.commit()
conn.close()

#updateSql =
        INSERT INTO `{0!s}`.`media` 
            (`path`, `name`, `type`, `size`, `mtime`) 
        VALUES 
            ({1!r}, {2!r}, 'File', {3!s}, {4!s}) 
        ON DUPLICATE KEY UPDATE 
            `size` = VALUES(`size`), 
            `mtime` = VALUES(`mtime`),
            `updated` = NOW();
    ### print '\n [+] newbornMQdata:\n {!r}'.format(newbornMQdata)
    ### print '\n [-] obsoleteDBdata:\n {!r}'.format(obsoleteDBdata)
"""