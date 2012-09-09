# -*- coding: utf-8 -*- 
'''
@summary: AssetManagement main
@since: 2012.08.26
@version: 0.0.2
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    Smart reduce sequence media list
"""
# ---------------------------------------------------------------------------------------------
# CHANGELOG
# ---------------------------------------------------------------------------------------------
'''
    ...
'''
import sys ###
import pprint ###

import os
from stat import ( S_ISDIR, S_ISREG )
# import re


# cfgScanRoot = "c:\_GitHub\pySequenceTester\test4"
cfgScanRoot = "d:\\dev.Git\\pyAssetManagement\\test1"
if len( sys.argv ) > 1: ### 
    cfgScanRoot = sys.argv[1] ###
print '\ncfgStorageRoot:', cfgScanRoot, '\n------------' ###


# tuples with media file extentions (lower-case!)
cfgFileMediaExt = '.mov', '.avi', '.mp4'
cfgSequenceMediaExt = '.dpx', '.tif', '.jpg', '.png'

# set and compile regExp 
#cfgRePattern = '^(.*\D)?(\d+)?(\.[^\.]+)$' # modified '^(.*\D)?(\d+)?(\.[^\.]+)$'
#cfgReCompiled = re.compile( cfgRePattern, re.I ) 

varRawDirList = [] # list for folder's items
varRawDirListInfo = [] # list for folder's items info
varSubDirList = [] # list for folder's subfolders
varFileList = [] # list for folder's files

def sendMessageToQM( message, content = None ): # send message to MQ server
    # TODO make an agreement about message protocol
    print '\n### send to MQ:', message ###
    if content != None: ###
        print type( content ), ':', len( content ), ':' ###
    ### pprint.pprint( content ) ###
    pass

def getRawDirList( RootFolder ): # let's read raw directory listing
    try: 
        rawDirList = os.listdir( RootFolder )
    except:
        # TODO: log exception
        return False
    # TODO: log info listing
    return rawDirList

def getRawDirListInfo( RootFolder, FolderListing ):
    rawDirListInfo = [] # list for collected item's data
    # collect stat info
    for item in FolderListing:
        itemStat = os.stat( RootFolder + os.sep +  item ) 
        # string concatenation instead os.path.join( RootFolder, item )
        itemInfo = {} # create dummy dict for collected values 
        itemInfo['path'] = cfgScanRoot
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

def isFileMedia( listItem ):
    # check if lower-cased name ends with one of the 'file media extentions' tuple's values
    return listItem['name'].lower().endswith( cfgFileMediaExt )

def isSequenceMedia( listItem ):
    # check if lower-cased name ends with one of the 'sequence media extentions' tuple's values
    return listItem['name'].lower().endswith( cfgSequenceMediaExt )


if __name__ == '__main__':
    # get raw directory list 
    varRawDirList = getRawDirList( cfgScanRoot )
    # exit if something wrong
    if varRawDirList == False:
        sendMessageToQM('Ooops! Folder is gone', cfgScanRoot ) # current scan folder
        exit( 0 ) # raise SystemExit with the 0 exit code.
    
    # get stat info about raw directory list items
    varRawDirListInfo = getRawDirListInfo( cfgScanRoot, varRawDirList )
    # sort out collected info to subfolders / files list
    varSubDirList, varFileList = sortOutCollected( varRawDirListInfo )
    
    # push SUBFOLDERS info message to MQ, if any
    if len( varSubDirList ) > 0:
        sendMessageToQM( 'Subfolders found', varSubDirList ) # subfolders list
    else: # if empty
        sendMessageToQM( 'NO Subfolders found', cfgScanRoot ) # current scan folder
    
    # filter file-type media
    varFileMediaList = filter( isFileMedia, varFileList )
    
    # push FILE-MEDIA info message to MQ, if any
    if len( varFileMediaList ) > 0:
        sendMessageToQM( 'File-media found', varFileMediaList ) # file-based media files list
    else: # if empty
        sendMessageToQM( 'NO File-media found', cfgScanRoot ) # current scan folder
    
    # filter sequence-type media
    varSequenceMediaList = filter( isSequenceMedia, varFileList )
    
    # TODO smart reduce sequence media list
    
    
    # push SEQUENCE-MEDIA info message to MQ, if any
    if len( varSequenceMediaList ) > 0:
        sendMessageToQM('Sequence-media found', varSequenceMediaList ) # sequence-based media files list
    else: # if empty 
        sendMessageToQM('NO Sequence-media found', cfgScanRoot  ) # current scan folder
    

    pass