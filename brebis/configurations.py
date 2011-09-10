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

#Parse the configurations
'''Parse the configurations'''

import sys
from configparser import ConfigParser
from configparser import ParsingError, NoSectionError, NoOptionError
import os

class Configurations:
    '''Retrieve the different configurations'''

    def __init__(self, __confpath):
        '''The constructor of the Configurations class.

        __confpath -- the path to the directory with the configuration files

        '''
        self.__configs = {}
        self.__parse_configurations(__confpath)

    def __parse_configurations(self, __confpath):
        '''Parse the different configurations'''
        try:
            __confs = [__file for __file in os.listdir(__confpath) 
                if __file.endswith('.conf')]
            for __conf in __confs:
                __currentconf = {}
                __config = ConfigParser()
                __fullconfpath = os.path.join('/'.join([__confpath, __conf]))
                with open(__fullconfpath, 'r') as __file:
                    __config.read_file(__file)
                # Common information for the backups
                ### The type of the backups
                __currentconf['type'] = __config.get('main', 'type')
                # Common information for the archives
                ### The archive path
                __confsettings = [{'main': 'path'},
                ### The list of the expected files in the archive
                {'main': 'files_list'}
                ]
                for __element in __confsettings:
                    __key, __value = __element.popitem()
                    if __config.has_option(__key, __value):
                        __currentconf[__value] = __config.get(
                                                    __key, __value)
                    else:
                        __currentconf[__value] = __config.set(
                                                    __key, __value, '')
                # Checking the information
                ### Check the paths in the configuration
                __confkeys= ('path', 'files_list')
                for __confkey in __confkeys:
                    __path = __currentconf[__confkey]
                    if not __path:
                        print('A path is missing in {}.'.format(__config.get('main', 'name')))
                        sys.exit(1)
                    if not os.path.isabs(__path):
                        __path = os.path.normpath(os.path.join(os.path.abspath(__confpath), __path))
                        __currentconf[__confkey] = __path
                    if not os.path.exists(__path):
                        print('{} does not exist.'.format(__path))
                        sys.exit(1)

                # check if the name of the conf does not exist yet
                if __config.get('main', 'name') in self.__configs:
                    print('The configuration name in {} already exists. Please rename it.'.format(__fullconfpath))
                    sys.exit(1)
                else:
                    self.__configs[__config.get('main', 'name')] = __currentconf
        except (ParsingError, NoSectionError, NoOptionError, OSError, IOError) as __err:
            print(__err)
            sys.exit(1)

    @property
    def configs(self):
        '''Return the different configurations parameters'''
        return self.__configs