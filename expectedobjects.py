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

# Extract the information about expected objects
'''Extract the information about expected objects'''

import sys

class ExpectedObjects(object):
    '''Extract the information about expected objects'''

    def __init__(self, __path):
        self._db_objects = {}
        self._main(__path)

    def _main(self, __path):
        '''Main of the ExpectedObjects class'''
        try:
            with open(__path, 'r') as __file:
                self._retrieve_data(__file)
        except (IOError, OSError) as __err:
            print(__err)
            sys.exit(1)
