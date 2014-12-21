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

import lzma
import os
import os.path
import stat

from brebis.checkhashes import get_hash
from brebis.generatelist.generatelist import GenerateList

# Generate a list of files from a lzma archive
'''Generate a list of files from a lzma archive'''

class GenerateListForLzma(GenerateList):
    '''Generate a list of files from a lzma archive'''

    def __init__(self, __genparams):
        '''The constructor for the GenerateListForlzma class'''
        __arcpath = __genparams['arcpath']
        __delimiter = __genparams['delimiter']
        self._genfull = __genparams['genfull']
        self.__confoutput = __genparams['confoutput']
        self.__listoutput = __genparams['listoutput']
        self.__fulloutput  = __genparams['fulloutput']
        self.__getallhashes  = __genparams['getallhashes']
        self.__hashtype = __genparams['hashtype']
        __listoffiles = ['[files]\n']
        __filetype = 'f'
        __filehash = get_hash(lzma.LZMAFile(__arcpath, 'r'), 'md5')
        if self.__getallhashes:
            if not self.__hashtype:
                __onelinewithhash = '{value}{delimiter} type{delimiter}{value} md5{delimiter}{value}\n'.format(value='{}', delimiter=__delimiter)
            else:
                __onelinewithhash = '{value}{delimiter} type{delimiter}{value} {hashtype}{delimiter}{value}\n'.format(value='{}', hashtype=self.__hashtype, delimiter=__delimiter)
            __listoffiles.append(__onelinewithhash.format(
                                    os.path.split(__arcpath)[-1][:-3],
                                    __filetype,
                                    __filehash))
        else:
            __onelinewithouthash = '{value}{delimiter} type{delimiter}{value}\n'.format(value='{}', delimiter=__delimiter)
            __listoffiles.append(__onelinewithouthash.format(
                                    os.path.split(__arcpath)[-1][:-3],
                                    __filetype))

        # define the flexible file list path
        __arcwithext = os.path.split(''.join([__arcpath[:-2], 'list']))[1]
        if self.__listoutput:
            __arclistpath = os.path.join(self.__listoutput, __arcwithext)
        elif self.__fulloutput:
            __arclistpath = os.path.join(self.__fulloutput, __arcwithext)
        else:
            # default
            __arclistpath = ''.join([__arcpath[:-2], 'list'])

        # call the method to write information in a file
        __listconfinfo = {'arclistpath': __arclistpath,
                            'listoffiles':  __listoffiles}
        self._generate_list(__listconfinfo)
        # call the method to write the configuration file if --gen-full was required
        if self._genfull:
            # generate the hash sum of the list of files
            __listhashsum = self._get_list_hash(__listconfinfo['arclistpath'])
            # define the flexible configuration file path
            __arcwithext = os.path.split(''.join([__arcpath[:-2], 'conf']))[1]
            if self.__confoutput:
                __arcconfpath = os.path.join(self.__confoutput, __arcwithext)
            elif self.__fulloutput:
                __arcconfpath = os.path.join(self.__fulloutput, __arcwithext)
            else:
                # default
                __arcconfpath = ''.join([__arcpath[:-2], 'conf'])
            __arcname =  os.path.basename(__arcpath[:-3])
            __confinfo = {'arcname': __arcname,
                            'arcpath': __arcpath,
                            'arcconfpath': __arcconfpath,
                            'arclistpath': __listconfinfo['arclistpath'],
                            'arctype': 'archive',
                            'sha512': __listhashsum}
            self._generate_conf(__confinfo)
