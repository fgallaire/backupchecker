# -*- coding: utf-8 -*-
# Copyright © 2009 Carl Chenet <chaica@ohmytux.com>
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

# Extract the information about expected saved files
'''Extract the information about expected saved files'''

import logging
import os
import sys

class ExpectedFiles(object):
    '''Extract the information about expected saved files'''

    def __init__(self, __path):
        self.__data = []
        self.__main(__path)

    def __main(self, __path):
        '''Main of the ExpectedFiles class'''
        try:
            with open(__path, 'r') as __file:
                self.__retrieve_data(__file)
        except (IOError, OSError) as __err:
            print(__err)
            sys.exit(1)

    def __retrieve_data(self, __file):
        '''Retrieve data from the expected files'''
        for __line in __file.readlines():
            __data = {}
            __res = []
            if __line != os.linesep:
                __res = __line.split()
                __data['path'] = __res[0]
                if len(__res) >= 2:
                    for __arg in __res[1:]:
                        if __arg.startswith('='):
                            __data['equals'] = self.__convert_arg(__arg)
                        if __arg.startswith('>'):
                            __data['biggerthan'] = self.__convert_arg(__arg)
                        elif __arg.startswith('<'):
                            __data['smallerthan'] = self.__convert_arg(__arg)
            self.__data.append(__data)

    def __convert_arg(self, __arg):
        '''Convert the given file length to bytes'''
        try:
            if __arg.endswith('K'):
                __res = int(__arg[1:-1]) * 1024
            elif __arg.endswith('M'):
                __res = int(__arg[1:-1]) * 1024**2
            elif __arg.endswith('G'):
                __res = int(__arg[1:-1]) * 1024**3
            elif __arg.endswith('P'):
                __res = int(__arg[1:-1]) * 1024**4
            elif __arg.endswith('E'):
                __res = int(__arg[1:-1]) * 1024**5
            elif __arg.endswith('Z'):
                __res = int(__arg[1:-1]) * 1024**6
            elif __arg.endswith('Y'):
                __res = int(__arg[1:-1]) * 1024**7
            else:
                __res = int(__arg[1:-1])
        except ValueError as __msg:
            logging.warn(__msg)
            __res = 0
        return __res

    @property
    def data(self):
        '''Return the paths of the expected files in the archive'''
        return self.__data
