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
from win32verstamp import Var
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
import pprint ###

import os
from stat import ( S_ISDIR, S_ISREG )
# import re


# cfgStorageRoot = "c:\_GitHub\pySequenceTester\test4"
cfgStorageRoot = "d:\\dev.Git\\pyAssetManagement\\test1"
if len( sys.argv ) > 1: ### 
    cfgStorageRoot = sys.argv[1] ###
print '\ncfgStorageRoot:', cfgStorageRoot, '\n------------' ###


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

def sendMessageToQM( label, content = None ): # send message to MQ server
    # TODO make an agreement about message protocol
    print '\n### send to MQ:', label ###
    if content != None: ###
        print type( content ), ':', len( content ), ':' ###
    ### pprint.pprint( content ) ###
    pass

def getRawDirList( RootFolder ): # let's read raw directory listing
    try: 
        rawDirList = os.listdir( RootFolder )
    except:
        # TODO: log exception
        # send exception message to MQ
        sendMessageToQM('Ooops! Folder is gone', RootFolder )
        return False
    # TODO: log info listing
    # print '### OK: items in folder ', RootFolder, ' : ', len( rawDirList ) ###
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

def isFileMedia( listItem ):
    # check if lower-cased name ends with one of the 'file media extentions' tuple's values
    return listItem['name'].lower().endswith( cfgFileMediaExt )

def isSequenceMedia( listItem ):
    # check if lower-cased name ends with one of the 'sequence media extentions' tuple's values
    return listItem['name'].lower().endswith( cfgSequenceMediaExt )


if __name__ == '__main__':
    # get raw directory list 
    varRawDirList = getRawDirList( cfgStorageRoot )
    # exit if something wrong
    if varRawDirList == False:
        exit( 0 ) # raise SystemExit with the 0 exit code.
    
    # get stat info about raw directory list items
    varRawDirListInfo = getRawDirListInfo( cfgStorageRoot, varRawDirList )
    # sort out collected info to subfolders / files
    varSubDirList, varFileList = sortOutCollected( varRawDirListInfo )
    
    # push SUBFOLDERS info message to MQ, if any
    if len( varSubDirList ) > 0:
        # TODO make an agreement about arguments list
        sendMessageToQM('Subfolders found', varSubDirList )
    # if empty
    else:
        # TODO make an agreement about arguments list
        sendMessageToQM('NO Subfolders found')
    
    # filter file-type media
    varFileMediaList = filter( isFileMedia, varFileList )
    
    # push FILE-MEDIA info message to MQ, if any
    if len( varFileMediaList ) > 0:
        # TODO make an agreement about arguments list
        sendMessageToQM('File-media found', varFileMediaList )
    # if empty
    else:
        # TODO make an agreement about arguments list
        sendMessageToQM('NO File-media found')
    
    # filter sequence-type media
    varSequenceMediaList = filter( isSequenceMedia, varFileList )
    
    # TODO smart reduce sequence media list
    
    
    # ### push SEQUENCE-MEDIA info message to MQ, if any
    if len( varSequenceMediaList ) > 0:
        # TODO make an agreement about arguments list
        sendMessageToQM('Sequence-media found', varSequenceMediaList )
    # if empty
    else: 
        # TODO make an agreement about arguments list
        sendMessageToQM('NO Sequence-media found' )
    
    '''
    print '\n varFileMedia:\t' + str( len( varFileMedia )) ###
    for item in varFileMedia:
        ### print item
        pass 
    '''
    pass