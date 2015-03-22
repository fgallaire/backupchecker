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

# Duration translation from human readable to datetime object
'''Duration translation'''

from datetime import timedelta
import sys

class Duration(object):
    '''Duration translation from human readable to timedelta object'''

    def __init__(self, __duration):
        '''The constructor for the Duration class.

        Keyword arguments:
        __duration -- duration in human-readable format

        '''
        if len(__duration.split()) != 2:
            print('Issue while parsing the duration - should be something like: 2 months')
            sys.exit(1)
        __nb, __word = __duration.split()
        try:
            __nb = int(__nb)
        except ValueError as __msg:
            print('Issue while parsing duration: {}'.format(__msg))
            sys.exit(1)
        if __word not in ('second', 'seconds', 'minute', 'minutes', 'hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years', 'decade', 'decades'):
            print('Issue while parsing duration: could not interpret {}'.format(__word))
            sys.exit(1)
        if 'second' in __word:
            self.__delta = timedelta(seconds=__nb)
        if 'minute' in __word:
            self.__delta = timedelta(minutes=__nb)
        if 'hour' in __word:
            self.__delta = timedelta(hours=__nb)
        if 'day' in __word:
            self.__delta = timedelta(days=__nb)
        if 'week' in __word:
            self.__delta = timedelta(weeks=__nb)
        if 'month' in __word:
            self.__delta = timedelta(days=__nb*30)
        if 'year' in __word:
            self.__delta = timedelta(days=__nb*52*7)
        if 'decade' in __word:
            self.__delta = timedelta(days=__nb*10**52*7)

    @property
    def durationdelta(self):
        '''Return the duration'''
        return self.__delta
