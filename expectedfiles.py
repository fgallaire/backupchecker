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
"""Extract the information about expected saved files"""

import logging
import os
import sys

class ExpectedFiles(object):
    """Extract the information about expected saved files"""

    def __init__(self, _path):
        self._data = []
        self.__main(_path)

    def __main(self, _path):
        """ Main of the ExpectedFiles class"""
        try:
            with open(_path, 'r') as _file:
                self.__retrieve_data(_file)
        except (IOError, OSError) as _err:
            print(_err)
            sys.exit(1)

    def __retrieve_data(self, _file):
        """Retrieve data from the expected files"""
        for _line in _file.readlines():
            _data = {}
            _res = []
            if _line != os.linesep:
                print('ok')
                _res = _line.split()
                _data['path'] = _res[0]
                if len(_res) >= 2:
                    for _arg in _res[1:]:
                        if _arg.startswith('='):
                            _data['equals'] = self.__convert_arg(_arg)
                        if _arg.startswith('>'):
                            _data['biggerthan'] = self.__convert_arg(_arg)
                        elif _arg.startswith('<'):
                            _data['smallerthan'] = self.__convert_arg(_arg)
            self._data.append(_data)

    def __convert_arg(self, _arg):
        "Convert the given file length to bytes"""
        try:
            if _arg.endswith('K'):
                _res = int(_arg[1:-1]) * 1024
            elif _arg.endswith('M'):
                _res = int(_arg[1:-1]) * 1024**2
            elif _arg.endswith('G'):
                _res = int(_arg[1:-1]) * 1024**3
            elif _arg.endswith('P'):
                _res = int(_arg[1:-1]) * 1024**4
            elif _arg.endswith('E'):
                _res = int(_arg[1:-1]) * 1024**5
            elif _arg.endswith('Z'):
                _res = int(_arg[1:-1]) * 1024**6
            elif _arg.endswith('Y'):
                _res = int(_arg[1:-1]) * 1024**7
            else:
                _res = int(_arg[1:-1])
        except ValueError as _msg:
            logging.info(_msg)
            _res = 0
        return _res

    @property
    def data(self):
        """Return the paths of the expected files in the archive"""
        return self._data
