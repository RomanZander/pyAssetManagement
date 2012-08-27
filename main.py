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

###
import sys
# import ConfigParser

# cfgStorageRoot = "d:\\dev.Git\\pyAssetManagement\\test1"
cfgStorageRoot = "d:\\dev.Git\\pySequenceTester\\test4"
cfgSwitch = ( len( sys.argv ) > 1) ###


varRawDirList = []
varRawDirListInfo = []
varSubDirList = []
varRawFileList = []

if __name__ == '__main__':
    '''
    # configuration reading
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read('base.cfg')
    cfgDevice = str( config.get( 'storage', 'device' ))
    cfgPath = str( config.get( 'storage', 'path' ))
    '''
    if cfgSwitch: ###
        cfgStorageRoot = sys.argv[1]
    print '\n' + 'cfgStorageRoot: ' + str( cfgStorageRoot ) ### 
    print 'cfgSwitch: ' + str( cfgSwitch ) ###
    print "------------" ###
    
    # read raw listing
    try: 
        varRawDirList = os.listdir( cfgStorageRoot )
    except:
        print "### Oops!: can't get listdir" ###
        # TODO: log exeption
        raise ValueError("Can't scan this folder: \n\t" + cfgStorageRoot)
    
    print 'len( varRawDirList ):\t' + str( len( varRawDirList )) + '\n' ###
    
    # collect stat info
    for item in varRawDirList:
        itemStat = os.stat( os.path.join( cfgStorageRoot, item ))
        itemInfo = {}
        itemInfo['path'] = cfgStorageRoot
        itemInfo['name'] = item 
        itemInfo['size'] = itemStat.st_size
        varRawDirListInfo.append(itemInfo) 
        
    print 'len( varRawDirListInfo ):\t' + str( len( varRawDirListInfo )) + '\n' ###
    print 'varRawDirListInfo[1]:\t' + str( varRawDirListInfo[1] ) + '\n' ###
    
    '''
    for rootdir, dirs, files in os.walk( cfgStorageRoot ):
        print rootdir
        print dirs
        print files
        print '========'
    ''' 
    pass