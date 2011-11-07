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

# Generate a list of files from a tar archive
'''Generate a list of files from a tar archive'''

import logging
import tarfile

from brebis.checkhashes import get_hash
from brebis.generatelist.generatelist import GenerateList

class GenerateListForTar(GenerateList):
    '''Generate a list of files from a tar archive'''

    def __init__(self, __arcpath):
        '''The constructor for the GenerateListForTar class'''
        self.__arcpath = __arcpath
        try:
            __tar = tarfile.open(self.__arcpath, 'r')
            self.__main(__tar)
        except tarfile.TarError as _msg:
            __warn = '. You should investigate for a data corruption.'
            logging.warn('{}: {}{}'.format(self.__arcpath, str(_msg), __warn))

    def __main(self, __tar):
        '''Main for the GenerateListForTar class'''
        __listoffiles = ['[files]\n']
        __oneline = '{}| size|{} uid|{} gid|{} mode|{} type|{}\n'
        __onelinewithhash = '{}| size|{} uid|{} gid|{} mode|{} type|{} md5|{}\n'
        for __tarinfo in __tar:
            # Pick up tar information
            __tarinfo.name = self._normalize_path(__tarinfo.name)
            __type = self.__translate_type(__tarinfo.type)
            __mode = oct(__tarinfo.mode).split('o')[-1]
            if __type == 'f':
                # extract hash sum of the file inside the archive
                __hash = get_hash(__tar.extractfile(__tarinfo.name), 'md5')
                # format the retrieved information
                __listoffiles.append(__onelinewithhash.format(__tarinfo.name,
                                                        str(__tarinfo.size),
                                                        str(__tarinfo.uid),
                                                        str(__tarinfo.gid),
                                                        __mode,
                                                        __type,
                                                        __hash))
            else:
                # if file is not regular file, ignoring its hash sum
                __listoffiles.append(__oneline.format(__tarinfo.name,
                                                        str(__tarinfo.size),
                                                        str(__tarinfo.uid),
                                                        str(__tarinfo.gid),
                                                        __mode,
                                                        __type))
        # Compose the name of the generated list
        if self.__arcpath.lower().endswith('.tar'):
            self.__arcpath = ''.join([self.__arcpath[:-3], 'list'])
        elif self.__arcpath.lower().endswith('.tar.gz'): 
            self.__arcpath = ''.join([self.__arcpath[:-6], 'list'])
        elif self.__arcpath.lower().endswith('.tar.bz2'):
            self.__arcpath = ''.join([self.__arcpath[:-7], 'list'])
        elif self.__arcpath.lower().endswith('.tgz'):
            self.__arcpath = ''.join([self.__arcpath[:-3], 'list'])
        elif __arcpath.lower().endswith('.tbz2'):
            self.__arcpath = ''.join([self.__arcpath[:-4], 'list'])
        # call the method to write information in a file
        self._generate_list(self.__arcpath, __listoffiles)

    def __translate_type(self, __arctype):
        '''Translate the type of the file inside the tar by a generic
        name
        '''
        __types = {tarfile.REGTYPE: 'f',
            tarfile.AREGTYPE: 'a',
            tarfile.CHRTYPE: 'c',
            tarfile.DIRTYPE: 'd',
            tarfile.LNKTYPE: 'l',
            tarfile.SYMTYPE: 's',
            tarfile.CONTTYPE: 'n',
            tarfile.BLKTYPE: 'b',
            tarfile.GNUTYPE_SPARSE: 'g',
            tarfile.FIFOTYPE: 'o'}
        return __types[__arctype]
