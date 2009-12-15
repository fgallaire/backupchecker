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

# Extract the information about expected database objects
'''Extract the information about expected database objects'''

import logging
import os
import sys

from expectedobjects import ExpectedObjects

class ExpectedDbObjects(ExpectedObjects):
    '''Extract the information about expected database objects'''

    def _retrieve_data(self, __file):
        '''Retrieve data from the expected database objects'''
        for __line in __file.readlines():
            __data = []
            __res = []
            if __line != os.linesep:
                __res = __line.split()
                if len(__res) >= 2:
                    if __res[0] == 'tables':
                        self._db_objects['tables'] = __res[1:]

    @property
    def db_objects(self):
        '''Return the paths of the expected files in the archive'''
        return self._db_objects
