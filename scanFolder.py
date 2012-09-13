# -*- coding: utf-8 -*- 
'''
@summary: AssetManagement main
@since: 2012.08.26
@version: 0.0.6
@author: Roman Zander
@see:  https://github.com/RomanZander/pyAssetManagement
'''
# ---------------------------------------------------------------------------------------------
# TODO
# ---------------------------------------------------------------------------------------------
"""
    seriaize data before send
"""
# ---------------------------------------------------------------------------------------------
# CHANGELOG
# ---------------------------------------------------------------------------------------------
'''
    0.0.6 +
    0.0.5 +arg parsing (+logging options)
    0.0.4 +real path reconstruction
    0.0.3 +logging
    0.0.2 +Smart reduce sequence media list
'''
import sys ###
import pprint ###
import logging
import argparse
import os
from stat import (S_ISDIR, S_ISREG)
import re

# tuples with media file extentions (lower-case!)
cfgFileMediaExt = '.mov', '.avi', '.mp4'
cfgSequenceMediaExt = '.dpx', '.tif', '.jpg', '.png'

# set and compile regExp 
cfgRePattern = '^(.*\D)?(\d+)(\.[^\.]+)$' # modified '^(.*\D)?(\d+)?(\.[^\.]+)$'
cfgReCompiled = re.compile(cfgRePattern, re.I) 

cfgScanRoot = '' # scanning root folder
cfgLoglevel = '' # logging level
cfgLogfile = '' # logging file name

varRawDirList = [] # list for folder's items
varRawDirListInfo = [] # list for folder's items info
varSubDirList = [] # list for folder's subfolders
varFileList = [] # list for folder's files

def parseArgs(): # parse command line arguments
    global cfgScanRoot, cfgLoglevel, cfgLogfile
    
    # extract version string from __doc__
    versionStrings = [string for string in __doc__.split('@') if (string.startswith('version:'))]
    if len(versionStrings) > 0:
        versionString = versionStrings[0]
    else:
        versionString = ''
    
    # create parser and add arguments
    parser = argparse.ArgumentParser(description = 'folder scan script for AssetManagement')
    parser.add_argument( 
        '-v', '--version', 
        action = 'version', 
        version = '%(prog)s ' + versionString
        )
    parser.add_argument( 
        'scanRoot',
        nargs = '?',
        default = '.',
        metavar = 'FOLDERPATH', 
        help = 'folder path to scan, "." by default' 
        )
    parser.add_argument( 
        '-l', '--log',
        default = '.log',
        dest = 'logLevel',
        metavar = 'INFO',
        help = 'set valid logging level (i.e. INFO)' 
        )
    parser.add_argument( 
        '-f', '--file',
        default = None,
        dest = 'logFile',
        metavar = 'FILENAME.LOG',
        help = 'set log file name' 
        )
    args = parser.parse_args()    
    
    # re-set global vars
    cfgScanRoot = os.path.realpath(args.scanRoot) # real path reconstruction
    cfgLoglevel = args.logLevel
    cfgLogfile = args.logFile
    pass

def configLogging():
    global cfgLoglevel, cfgLogfile
    #get logging level
    logLevelNumeric = getattr(logging, cfgLoglevel.upper(), None)
    if isinstance(logLevelNumeric, int): # if logging level is valid
        # set logging level and format
        if cfgLogfile: # if not empty
            # config log to file
            logging.basicConfig(
                                filename = cfgLogfile, 
                                filemode = 'a',
                                level = logLevelNumeric, 
                                format = '===\n%(levelname)s | %(asctime)s | %(message)s'
                                )
        else: # if empty
            # config log to screen only
            logging.basicConfig(
                                level = logLevelNumeric, 
                                format = '===\n%(levelname)s | %(asctime)s | %(message)s'
                                )
        ### logging.basicConfig(filename='example.log', filemode='w')
        # logging.basicConfig(level=logLevelNumeric, format='===\n%(levelname)s | %(asctime)s | %(message)s')
        
    pass

def sendMessageToQM(message, content = None): # send message to MQ server
    # TODO make an agreement about message protocol
    # QM code here
    logging.info('send to MQ:\n%s\n%s\n', message, content) 

    pass

def getRawDirList(RootFolder): # let's read raw directory listing
    try: 
        rawDirList = os.listdir(RootFolder)
    except:
        # TODO: log exception
        return False
    # TODO: log info listing
    return rawDirList

def getRawDirListInfo(RootFolder, FolderListing):
    rawDirListInfo = [] # list for collected item's data
    # collect stat info
    for item in FolderListing:
        itemStat = os.stat(RootFolder + os.sep +  item) 
        # string concatenation instead os.path.join( RootFolder, item )
        itemInfo = {} # create dummy dict for collected values 
        itemInfo['path'] = cfgScanRoot
        itemInfo['name'] = item 
        itemInfo['mode'] = itemStat.st_mode
        itemInfo['size'] = itemStat.st_size
        itemInfo['mtime'] = itemStat.st_mtime
        rawDirListInfo.append(itemInfo)
    return rawDirListInfo

def sortOutCollected(rawDirListInfo):
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
        if S_ISDIR(itemInfo['mode']):
            subDirList.append(outItem)
        # else if item is file append output item to files list
        elif S_ISREG(itemInfo['mode']):
            fileList.append(outItem)
    # returns tuple of folders / files lists
    return  (subDirList, fileList)

def isFileMedia(listItem):
    # check if lower-cased name ends with one of the 'file media extentions' tuple's values
    return listItem['name'].lower().endswith(cfgFileMediaExt)

def isSequenceMedia(listItem):
    # check if lower-cased name ends with one of the 'sequence media extentions' tuple's values
    return listItem['name'].lower().endswith(cfgSequenceMediaExt)

def isMatchPattern(listItem):
    # tests item's 'name' dict value by name convention regexp pattern
    return cfgReCompiled.match(listItem['name'])
 
def smartSortSplittedName(a, b):
    # custom compare for sort by file extention, then by file prefix, then by file index
    aListed = [a['nameExtention'], a['namePrefix'], a['nameIndex']]
    bListed = [b['nameExtention'], b['namePrefix'], b['nameIndex']]
    if aListed > bListed:
        return 1
    elif aListed == bListed:
        return 0
    else:
        return -1
 
def smartReduceMediaList(sequenceMediaList):
    # filter by naming convention compliance
    namingConventionMatched = filter(isMatchPattern, sequenceMediaList)
    
    # build splitted file list (splitted by extention, filename prefix and file index)
    splittedNameList = []
    for item in namingConventionMatched:
        # build up data for sort with regexp
        splittedNameList.append({
                                 'path': item['path'],
                                 'namePrefix': cfgReCompiled.match(item['name']).group(1),
                                 'nameIndex': cfgReCompiled.match(item['name']).group(2),
                                 'nameExtention': cfgReCompiled.match(item['name']).group(3),
                                 'size':item['size'],
                                 'mtime':item['mtime'] 
                                 })
    # custom sort splitted file list
    splittedNameList.sort(cmp = smartSortSplittedName)
    
    # recollect by extention
    collectedSequences = []
    lastToCompare = None
    for splittedNameItem in splittedNameList:
        
        # 1st iteration
        if lastToCompare == None:
            # remember 1st for follow comparison
            lastToCompare = { 
                             'namePrefix': splittedNameItem['namePrefix'],
                             'nameIndex': splittedNameItem['nameIndex'],
                             'nameExtention': splittedNameItem['nameExtention'],
                             }
            # store 1st element data
            collectedSequences.append( {
                                        'namePrefix': splittedNameItem['namePrefix'],
                                        'nameIndexStart': splittedNameItem['nameIndex'],
                                        'nameIndexFinish': splittedNameItem['nameIndex'],
                                        'nameExtention': splittedNameItem['nameExtention'],
                                        'size': splittedNameItem['size'],
                                        'mtime': splittedNameItem['mtime']
                                         } )
        
        # same extention and prefix, but +1 
        elif  (               
               splittedNameItem['namePrefix'] == lastToCompare['namePrefix'] and
               splittedNameItem['nameExtention'] == lastToCompare['nameExtention'] and
               int( splittedNameItem['nameIndex']) == int(lastToCompare['nameIndex']) + 1 
               ) :
            # get dictionary from last record:
            lastRecord = collectedSequences[len(collectedSequences) - 1]
            # modify sequence finish
            lastRecord['nameIndexFinish'] = splittedNameItem['nameIndex']
            # modify sequence size
            lastRecord['size'] = lastRecord['size'] + splittedNameItem['size']
            # modify sequence modification time, if later
            if lastRecord['mtime'] < splittedNameItem['mtime'] :
                lastRecord['mtime'] = splittedNameItem['mtime']
            # re-store data to last record
            collectedSequences[len(collectedSequences) - 1] = lastRecord
            # refresh remembered last
            lastToCompare = { 
                             'namePrefix': splittedNameItem['namePrefix'],
                             'nameIndex': splittedNameItem['nameIndex'],
                             'nameExtention': splittedNameItem['nameExtention'],
                             }
        
        # extention or prefix changed or not +1
        else:
            # store next element data
            collectedSequences.append({
                                       'namePrefix': splittedNameItem['namePrefix'],
                                       'nameIndexStart': splittedNameItem['nameIndex'],
                                       'nameIndexFinish': splittedNameItem['nameIndex'],
                                       'nameExtention': splittedNameItem['nameExtention'],
                                       'size': splittedNameItem['size'],
                                       'mtime': splittedNameItem['mtime']
                                        })
            # refresh remembered last
            lastToCompare = { 
                             'namePrefix': splittedNameItem['namePrefix'],
                             'nameIndex': splittedNameItem['nameIndex'],
                             'nameExtention': splittedNameItem['nameExtention'],
                             }
    return collectedSequences 

if __name__ == '__main__':
    
    parseArgs() # parse from command line
     
    configLogging() # logging setup 
    
    # logging output
    logging.info('cfgScanRoot:\n%s\n', cfgScanRoot) 
    
    # get raw directory list 
    varRawDirList = getRawDirList(cfgScanRoot)
    # exit if something wrong
    if varRawDirList == False:
        sendMessageToQM('Ooops! Folder is gone', cfgScanRoot) # current scan folder
        exit( 0 ) # raise SystemExit with the 0 exit code.
    
    # get stat info about raw directory list items
    varRawDirListInfo = getRawDirListInfo(cfgScanRoot, varRawDirList)
    # sort out collected info to subfolders / files list
    varSubDirList, varFileList = sortOutCollected(varRawDirListInfo)
    
    # push SUBFOLDERS info message to MQ, if any
    if len(varSubDirList) > 0:
        sendMessageToQM('Subfolders found', varSubDirList) # subfolders list
    else: # if empty
        sendMessageToQM('NO Subfolders found', cfgScanRoot) # current scan folder
    
    # filter file-type ('.mov', '.r3d' etc) media
    varFileMediaList = filter(isFileMedia, varFileList)
    
    # push FILE-MEDIA info message to MQ, if any
    if len(varFileMediaList) > 0:
        sendMessageToQM('File-media found', varFileMediaList) # file-based media files list
    else: # if empty
        sendMessageToQM('NO File-media found', cfgScanRoot) # current scan folder
    
    # filter sequence-type ('.dpx', '.jpg' etc with naming convention) media
    varSequenceMediaList = filter(isSequenceMedia, varFileList)
    
    # smart reduce sequence media list
    varReducedSequenceMediaList = smartReduceMediaList(varSequenceMediaList)
    
    # push SEQUENCE-MEDIA info message to MQ, if any
    if len(varReducedSequenceMediaList) > 0:
        sendMessageToQM('Sequence-media found', varReducedSequenceMediaList) # sequence-based media files list
    else: # if empty 
        sendMessageToQM('NO Sequence-media found', cfgScanRoot) # current scan folder
    

    pass