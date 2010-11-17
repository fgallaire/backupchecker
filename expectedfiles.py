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
import configparser
from configparser import ParsingError, NoSectionError, NoOptionError

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
        __config = configparser.ConfigParser()
        __config.readfp(__file)
        __files = __config.items('files')
        for __fileitems in __files:
            __data = {}
            __data['path'] = __fileitems[0]
            if len(__fileitems) == 2:
                for __item in __fileitems[1].split(' '):
                    try:
                        # Testing the items for an expected file
                        if __item == 'unexpected':
                            __data['unexpected'] = True
                        # The uid of the expected file
                        elif __item.startswith('uid:'):
                            __data['uid'] = int(__item.split(':')[-1])
                        # The gid of the expected file
                        elif __item.startswith('gid:'):
                            __data['gid'] = int(__item.split(':')[-1])
                        # The mode of the expected file
                        elif __item.startswith('mode'):
                            __mode =__item.split(':')[-1]
                            if len(__mode) < 3 or len(__mode) > 4:
                                logging.warn('{}: Wrong format for the mode.'.format(__data['path']))
                            else:
                                __data['mode'] = __mode
                        # Testing the type of the file
                        elif __item.startswith('type'):
                            __type =__item.split(':')[-1]
                            ### f for file, c for character, d for directory
                            ### s for symbolink link, b for block, o for fifo,
                            ### k for socket
                            __types = ('f','c','d','s','b','o','k')
                            if __type not in __types:
                                logging.warn('{}: Unknown type {} for file parameter'.format(__data['path'], __type))
                            else:
                                __data['type'] = __type
                        # Testing the size of the file
                        ### Test if the equality is required
                        elif __item.startswith('='):
                            __data['equals'] = self.__convert_arg(__item)
                        ### Test if bigger than is required
                        elif __item.startswith('>'):
                            __data['biggerthan'] = self.__convert_arg(__item)
                        ### Test if smaller than is required
                        elif __item.startswith('<'):
                            __data['smallerthan'] = self.__convert_arg(__item)
                    except ValueError as __msg:
                        logging.warn(__msg)
            self.__data.append(__data)

    def __convert_arg(self, __arg):
        '''Convert the given file length to bytes'''
        try:
            __res = int(__arg[1:-1])
            for __value, __power in [('K', 1),('M', 2),('G', 3),('P', 4),
                                        ('E', 5),('Z', 6),('Y', 7)]:
                if __arg.endswith(__value):
                    __res = int(__arg[1:-1]) * 1024**__power
        except ValueError as __msg:
            print(__msg)
            logging.warn(__msg)
            __res = 0
        finally:
            return __res

    @property
    def data(self):
        '''Return the paths of the expected files in the archive'''
        return self.__data
