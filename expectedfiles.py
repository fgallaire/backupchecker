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

import sys

class ExpectedFiles(object):
    """Extract the information about expected saved files"""

    def __init__(self, _path):
        self._paths = []
        self.__main(_path)

    def __main(self, _path):
        """ Main of the ExpectedFiles class"""
        try:
            with open(_path, 'r') as _file:
                self._paths = [_fpath.rstrip() for _fpath
                    in _file.readlines()]
        except (IOError, OSError) as _err:
            print(_err)
            sys.exit(1)

    @property
    def paths(self):
        """Return the paths of the expected files in the archive"""
        return self._paths
