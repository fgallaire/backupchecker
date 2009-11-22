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
import os

class Configurations:
    """Retrieve the different configurations"""

    def __init__(self, _confpath):
        self._configs = {}
        self.__parse_configurations(_confpath)

    def __parse_configurations(self, _confpath):
        """Parse the different configurations"""
        _confs = [_file for _file in os.listdir(_confpath) 
            if _file.endswith('.conf')]
        for _conf in _confs:
            _currentconf = {}
            try:
                _config = configparser.ConfigParser()
                _config.readfp(open(os.path.join(
                    '/'.join([_confpath, _conf])), 'r'))
                #currentconf['sources'] = config.get('main', 'md5')
                _currentconf['type'] = _config.get('main', 'type')
                _currentconf['path'] = _config.get('main', 'path')
                _currentconf['expected_file'] = _config.get('main', 'expected_file')
                # currentconf is a project, saved in a configuration dictionary
                self._configs[_config.get('main', 'name')] = _currentconf
                print(self._configs)
            except configparser.ParsingError as _err:
                print('Error while parsing {}'.format(_conf))
                sys.exit(1)
            except configparser.NoSectionError as _err:
                print('Error while parsing {}'.format(_conf))
                print('The mandatory [main] section is missing')
                sys.exit(1)
            except configparser.NoOptionError as _err:
                print('A mandatory option is missing')
                sys.exit(1)

    def return_configurations(self):
        """Return the different configurations parameteres"""
        return self._configs

