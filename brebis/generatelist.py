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


class GenerateList(object):
    '''The GenerateList class'''

    def _generate_list(self, __arcpath, __listoffiles):
        '''Generate a list of files inside the archive'''
        with open(__arcpath, 'w') as __arc:
            __arc.writelines(__listoffiles)

