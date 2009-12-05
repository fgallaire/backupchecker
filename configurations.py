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

#Parse the configurations
"""Parse the configurations"""

import sys
import configparser
from configparser import ParsingError, NoSectionError, NoOptionError
import os

class Configurations:
    """Retrieve the different configurations"""

    def __init__(self, __confpath):
        self.__configs = {}
        self.__parse_configurations(__confpath)

    def __parse_configurations(self, __confpath):
        """Parse the different configurations"""
        __confs = [__file for __file in os.listdir(__confpath) 
            if __file.endswith('.conf')]
        for __conf in __confs:
            __currentconf = {}
            try:
                __config = configparser.ConfigParser()
                __config.readfp(open(os.path.join(
                    '/'.join([__confpath, __conf])), 'r'))
                __currentconf['type'] = __config.get('main', 'type')
                __currentconf['path'] = __config.get('main', 'path')
                __currentconf['files_list'] = __config.get('main', 'files_list')
                __bckpath = os.path.abspath(__currentconf['path'])
                if not os.path.exists(__bckpath):
                    print('{} does not exists.'.format(__bckpath))
                    sys.exit(1)
                else:
                    self.__configs[__config.get('main', 'name')] = __currentconf
            except (ParsingError, NoSectionError, NoOptionError) as __err:
                print(__err)
                sys.exit(1)

    @property
    def configs(self):
        """Return the different configurations parameteres"""
        return self.__configs

