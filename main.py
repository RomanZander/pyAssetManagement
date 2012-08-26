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
    read config
"""
# ---------------------------------------------------------------------------------------------
# CHANGELOG
# ---------------------------------------------------------------------------------------------
'''
    ...
'''
import os
import ConfigParser

if __name__ == '__main__':
    # configuration reading
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read('base.cfg')
    cfgDevice = str( config.get( 'storage', 'device' ))
    cfgPath = str( config.get( 'storage', 'path' ))
    
    ###
    print cfgDevice
    print cfgPath 
    print "\n------------"
    for rootdir, dirs, files in os.walk( cfgDevice + cfgPath ):
        print rootdir
        print dirs
        print files
        print '========'
        
    
    

    pass