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

# Generate a list of files in a backup
'''Generate a list of files in a backup'''

import logging
import os.path
import sys

class GenerateList:
    '''The GenerateList class'''

    def _generate_list(self, __arcpath, __listoffiles):
        '''Write the list of file information inside the archive in a file'''
        try:
            with open(__arcpath, 'w') as __file:
                __file.writelines(__listoffiles)
        except (OSError, IOError) as __msg:
            print(__msg)
            sys.exit(1)

    def _normalize_path(self, __path):
        '''Remove last slash of a directory path if present'''
        if __path.endswith('/'):
            return __path[:-1]
        else:
            return __path
