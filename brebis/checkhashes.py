# -*- coding: utf-8 -*-
# Copyright © 2011 Carl Chenet <chaica@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Check the files hashes
'''Check the files hashes'''

import hashlib
import logging
import os.path
import sys

class CheckHashes(object):
    '''Check the files hashes of the backups'''

    def __init__(self, __hashfile, __hashtype, __confs):
        '''Constructor for the CheckHashes class.
        
        Keywork arguments:
        __hashfile -- the hashfile path
        __hashtype -- the type of the hash sum
        __confs -- a configuration object with the different archive paths        
        
        '''
        self.__confs = __confs
        self.__main(__hashfile, __hashtype, __confs)

    def __main(self, __hashfile, __hashtype, __confs):
        '''Main for the CheckHashes class.'''
        __hashinfo = self.__extract_hashinfo(__hashfile)
        self.__check_hashes(__hashtype, __confs, __hashinfo)

    def __check_hashes(self, __hashtype, __confs, __hashinfo):
        '''check the hash of the backups.'''
        try:
            __confstoremove = []
            for __conf in __confs:
                __bckname = os.path.split(__confs[__conf]['path'])[-1]
                if __bckname in __hashinfo:
                    with open(__confs[__conf]['path'], 'rb') as __file:
                        __res = getattr(hashlib, __hashtype)(
                            __file.read()).hexdigest()
                        if __res != __hashinfo[__bckname]:
                            logging.warn('The {} checksum mismatched'.format(
                                __confs[__conf]['path']))
                            __confstoremove.append(__conf)
            for __conf in __confstoremove:
                del(self.__confs[__conf])
        except (OSError, IOError) as __msg:
            logging.warn(__msg)

    def __extract_hashinfo(self, __hashfile):
        '''Extract the info about hash sums.'''
        __hashinfo = {}
        try:
            with open(__hashfile) as __files:
                for __file in __files:
                    __data = __file.split()
                    if len(__data) != 2:
                        __warning = '{}: invalid hash format file'
                        logging.warn(__warning.format(__hashfile))
                        sys.exit(1)
                    else:
                        __hashinfo[__data[-1]] = __data[0]
        except (OSError, IOError) as __msg:
            print(__msg)
            sys.exit(1)
        return __hashinfo
        
    @property
    def confs(self):
        '''Return the configurations minus the ones containing a 
        corrupted file.
        '''
        return self.__confs

def get_hash(__arcfile, __hashtype):
    '''return the hash of a file.'''
    __res = getattr(hashlib, __hashtype)(__arcfile.read()).hexdigest()
    __arcfile.close()
    return __res
    
