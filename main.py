# -*- coding: utf-8 -*- 
'''
@summary: AssetManagement main
@since: 2012.08.26
@version: 0.0.1
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    raw list dir
"""
# ---------------------------------------------------------------------------------------------
# CHANGELOG
# ---------------------------------------------------------------------------------------------
'''
    ...
'''
import os
from stat import *
import sys


cfgStorageRoot = "c:\_GitHub\pySequenceTester\test4"
# cfgStorageRoot = "d:\\dev.Git\\pySequenceTester\\test4"
cfgFileMediaExt = ['mov', 'avi']
cfgSeqenceMediaExt = ['dpx', 'tif']

varRawDirList = []
varRawDirListInfo = []
varSubDirList = []
varFileList = []

if __name__ == '__main__':

    if  ( len( sys.argv ) > 1 ): ###
        cfgStorageRoot = sys.argv[1] ###
    print '\n' + 'cfgStorageRoot: ' + str( cfgStorageRoot ) ### 
    print "------------" ###
    
    # read raw listing
    try: 
        varRawDirList = os.listdir( cfgStorageRoot )
    except:
        print "### Oops!: can't get listdir" ###
        # TODO: log exception
        raise ValueError("Can't scan this folder: \n\t" + cfgStorageRoot)
    
    print 'len( varRawDirList ):\t' + str( len( varRawDirList )) + '\n' ###
    
    # collect stat info
    for item in varRawDirList:
        itemStat = os.stat( os.path.join( cfgStorageRoot, item ))
        itemInfo = {}
        itemInfo['path'] = cfgStorageRoot
        itemInfo['name'] = item 
        itemInfo['mode'] = itemStat.st_mode
        itemInfo['size'] = itemStat.st_size
        itemInfo['mtime'] = itemStat.st_mtime
        varRawDirListInfo.append(itemInfo) 
        
    print 'len( varRawDirListInfo ):\t' + str( len( varRawDirListInfo )) + '\n' ###

    # sort out collected results
    for itemInfo in varRawDirListInfo:
        if S_ISDIR( itemInfo['mode'] ):
            varSubDirList.append( itemInfo )
        elif S_ISREG( itemInfo['mode'] ):
            varFileList.append( itemInfo )
         
    print '\nlen( varSubDirList ):\t' + str( len( varSubDirList )) ###
    for item in varSubDirList:
        print item 
    print '\nlen( varFileList ):\t' + str( len( varFileList )) ###
    for item in varFileList:
        print item 
    
    pass