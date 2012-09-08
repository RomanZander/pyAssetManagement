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
    qMessage "folder is gone"
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

varRawDirList = [] # list for folder's items
varRawDirListInfo = [] # list for folder's items info
varSubDirList = [] # list for folder's subfolders
varFileList = [] # list for folder's files

# let's read raw directory listing
def getRawDirList( RootFolder ):
    try: 
        rawDirList = os.listdir( RootFolder )
    except:
        # TODO: log exception
        # TODO: send exception message to MQ
        print "### Oops!: folder is gone: \t", RootFolder ###
        return False
        
    # TODO: log info listing
    print '### OK: items in folder ', RootFolder, ' : ', len( rawDirList ) ###
    
    return rawDirList

def getRawDirListInfo( RootFolder, FolderListing ):
    rawDirListInfo = [] # list for collected item's data
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
    return rawDirListInfo

def sortOutCollected( rawDirListInfo ):
    # init empty lists for folders / files
    subDirList = [] 
    fileList = []
    # iterate and sort out
    for itemInfo in rawDirListInfo:
        # create output item dictionary
        outItem = {'path':itemInfo['path'], 
                   'name':itemInfo['name'], 
                   'size':itemInfo['size'], 
                   'mtime':itemInfo['mtime']}
        # if item is folder append output item to folders list
        if S_ISDIR( itemInfo['mode'] ):
            subDirList.append( outItem )
        # else if item is file append output item to files list
        elif S_ISREG( itemInfo['mode'] ):
            fileList.append( outItem )
    # returns tuple of folders / files lists
    return  ( subDirList, fileList )

if __name__ == '__main__':
    
    
    ### dev-only: select argument 
    if  ( len( sys.argv ) > 1 ): ###
        cfgStorageRoot = sys.argv[1] ###
    print '\n' + 'cfgStorageRoot: ' + str( cfgStorageRoot ) ### 
    print "------------" ###
    ### /dev-only
    
    # get raw directory list 
    varRawDirList = getRawDirList( cfgStorageRoot )
    # exit if something wrong
    if varRawDirList == False:
        exit( 0 ) # raise SystemExit with the 0 exit code.
    # get stat info about raw directory list items
    varRawDirListInfo = getRawDirListInfo( cfgStorageRoot, varRawDirList )
    # sort out collected info to subfolders / files
    varSubDirList, varFileList = sortOutCollected( varRawDirListInfo )
    
    
         
    print '\nlen( varSubDirList ):\t' + str( len( varSubDirList )) ###
    
    for item in varSubDirList:
        print item
        pass 
    print '\nlen( varFileList ):\t' + str( len( varFileList )) ###
    for item in varFileList:
        print item
        pass 
    
    pass