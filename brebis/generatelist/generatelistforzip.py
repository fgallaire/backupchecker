# -*- coding: utf-8 -*-
# Copyright © 2013 Carl Chenet <chaica@ohmytux.com>
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

# Generate a list of files from a zip archive
'''Generate a list of files from a zip archive'''

import logging
import stat
import zipfile

from brebis.checkhashes import get_hash
from brebis.generatelist.generatelist import GenerateList

class GenerateListForZip(GenerateList):
    '''Generate a list of files from a zip archive'''

    def __init__(self, __arcpath):
        '''The constructor for the GenerateListForZip class'''
        self.__arcpath = __arcpath
        try:
            __zip = zipfile.ZipFile(self.__arcpath, 'r', allowZip64=True)
            self.__main(__zip)
        except zipfile.BadZipfile as _msg:
            __warn = '. You should investigate for a data corruption.'
            logging.warning('{}: {}{}'.format(__self.arcpath, str(__msg), __warn))

    def __main(self, __zip):
        '''Main of the GenerateListForZip class'''
        __listoffiles = ['[files]\n']
        __oneline = '{}| ={} uid|{} gid|{} mode|{} type|{}\n'
        __onelinewithhash = '{}| ={} uid|{} gid|{} mode|{} type|{} md5|{}\n'
        __crcerror = __zip.testzip()
        if __crcerror:
            logging.warning('{} has at least one file corrupted:{}'.format(self.__arcpath, __crcerror))
        else:
            __zipinfo = __zip.infolist()
            for __fileinfo in __zipinfo:
                __fileinfo.filename = self._normalize_path(__fileinfo.filename)
                # need to escape the default separator of the list of files
                __fileinfo.filename = self._escape_separator(__fileinfo.filename)
                __uid, __gid = self.__extract_uid_gid(__fileinfo)
                __type = self.__translate_type(__fileinfo.external_attr >> 16)
                __mode = oct(stat.S_IMODE((__fileinfo.external_attr >> 16))).split('o')[-1]
                if __type == 'f':
                    __hash = get_hash(__zip.open(__fileinfo.filename, 'r'), 'md5')
                    __listoffiles.append(__onelinewithhash.format(__fileinfo.filename,
                                                            str(__fileinfo.file_size),
                                                            str(__uid),
                                                            str(__gid),
                                                            __mode,
                                                            __type,
                                                            __hash))
                else:
                    __listoffiles.append(__oneline.format(__fileinfo.filename,
                                                            str(__fileinfo.file_size),
                                                            str(__uid),
                                                            str(__gid),
                                                            __mode,
                                                            __type))
        # Compose the name of the generated list
        self.__arcpath = ''.join([self.__arcpath[:-3], 'list'])
        # call the method to write information in a file
        self._generate_list(self.__arcpath, __listoffiles)

    def __extract_uid_gid(self, __binary):
        '''Extract uid and gid from a zipinfo.extra object (platform dependant)'''
        __uid, __gid = int.from_bytes(__binary.extra[15:17], 'little'), \
                            int.from_bytes(__binary.extra[20:22], 'little')
        return (__uid, __gid)

    def __translate_type(self, __mode):
        '''Translate the type of the file to a generic name'''
        if stat.S_ISREG(__mode):
            return 'f'
        elif stat.S_ISDIR(__mode):
            return 'd'
