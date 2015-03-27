# -*- coding: utf-8 -*-
# Copyright © 2015 Carl Chenet <chaica@backupcheckerproject.org>
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

# Identify and replace placeholder in a path
'''Identify and replace placeholder in a path'''

from datetime import datetime

class PlaceHolder(object):
    '''Identify and replace placeholder in a path'''

    def __init__(self, __path):
        '''The constructor for the PlaceHolder class.

        Keyword arguments:
        __path -- the path of the backup

        '''
        self.__path = __path
        self.__main()

    def __main(self):
        '''Main of the PlaceHolder class'''
        __year, __shortyear, __month, __day, __hour, __minute, __second = datetime.now().strftime('%Y %y %m %d %H %M %S').split()
        if '%Y' in self.__path:
            self.__path = self.__path.replace('%Y', __year)
        if '%y' in self.__path:
            self.__path = self.__path.replace('%y', __year)
        if '%m' in self.__path:
            self.__path = self.__path.replace('%m', __year)
        if '%d' in self.__path:
            self.__path = self.__path.replace('%d', __year)
        if '%H' in self.__path:
            self.__path = self.__path.replace('%H', __year)
        if '%M' in self.__path:
            self.__path = self.__path.replace('%M', __year)
        if '%S' in self.__path:
            self.__path = self.__path.replace('%S', __year)

    @property
    def realpath(self):
        '''Return the real path afther placeholder replacement'''
        return self.__path
