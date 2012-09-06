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
import sys ###

import os
from stat import ( S_ISDIR, S_ISREG )
import re


# cfgStorageRoot = "c:\_GitHub\pySequenceTester\test4"
# cfgStorageRoot = "d:\\dev.Git\\pySequenceTester\\test4"
cfgStorageRoot = "d:\\dev.Git\\pyAssetManagement\\test1"

# tuples with media file extentions 
cfgFileMediaExt = '.mov', '.avi'
cfgSeqenceMediaExt = '.dpx', '.tif', '.jpg'

# set and compile regExp 
cfgRePattern = '^(.*\D)?(\d+)?(\.[^\.]+)$' # modified '^(.*\D)?(\d+)?(\.[^\.]+)$'
### cfgReCompiled = re.compile( cfgRePattern, re.I ) 

varRawDirList = []
varRawDirListInfo = []
varSubDirList = []
varFileList = []

# let's read raw directory listing
def getRawDirList( RootFolder ):
    try: 
        rawDirList = os.listdir( RootFolder )
    except:
        print "### Oops!: can't get listdir \n\t" + RootFolder ###
        # TODO: log exception
        # ValueError("Can't scan this folder: \n\t" + Folder)
        raise ValueError 
        
    # TODO: log info listing
    print 'len( rawDirList ):\t' + str( len( rawDirList )) + '\n' ###
    
    return rawDirList
    pass

def getRawDirListInfo( RootFolder, FolderListing ):
    rawDirListInfo = []
    # collect stat info
    for item in FolderListing:
        itemStat = os.stat( RootFolder + os.sep +  item ) 
        # string concatenation instead os.path.join( RootFolder, item )
        itemInfo = {} # create dummy dict for collected values 
        itemInfo['path'] = cfgStorageRoot
        itemInfo['name'] = item 
        itemInfo['mode'] = itemStat.st_mode
        itemInfo['size'] = itemStat.st_size
        itemInfo['mtime'] = itemStat.st_mtime
        rawDirListInfo.append( itemInfo )
         
    # TODO: log collected info    
    print 'len( rawDirListInfo ):\t' + str( len( rawDirListInfo )) + '\n' ###
    
    return rawDirListInfo
    pass

if __name__ == '__main__':

    if  ( len( sys.argv ) > 1 ): ###
        cfgStorageRoot = sys.argv[1] ###
    print '\n' + 'cfgStorageRoot: ' + str( cfgStorageRoot ) ### 
    print "------------" ###
    
    # get raw directory list 
    varRawDirList = getRawDirList( cfgStorageRoot )

    # get stat info about raw directory list items
    varRawDirListInfo = getRawDirListInfo( cfgStorageRoot, varRawDirList )

    # sort out collected results
    for itemInfo in varRawDirListInfo:
        if S_ISDIR( itemInfo['mode'] ):
            varSubDirList.append( itemInfo )
        elif S_ISREG( itemInfo['mode'] ):
            varFileList.append( itemInfo )
         
    print '\nlen( varSubDirList ):\t' + str( len( varSubDirList )) ###
    
    for item in varSubDirList:
        #print item
        pass 
    print '\nlen( varFileList ):\t' + str( len( varFileList )) ###
    for item in varFileList:
        #print item
        pass 
    
    pass