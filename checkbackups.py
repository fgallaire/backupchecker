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

# Check the given backups
'''Check the given backups'''

import logging
from tarfile import is_tarfile
from zipfile import is_zipfile

from archiveinfomsg import ArchiveInfoMsg
from checktar import CheckTar
from checktree import CheckTree
from checkzip import CheckZip

class CheckBackups(object):
    '''The backup checker class'''

    def __init__(self, __confs):
        self.__main(__confs)

    def __main(self, __confs):
        '''Main for CheckBackups'''
        __cfgsets = __confs.values()
        for __cfgvalues in __cfgsets:
            # check a file tree
            if __cfgvalues['type'] == 'tree':
                __bck = CheckTree(__cfgvalues)
            # check a tar file
            elif __cfgvalues['type'] == 'archive' and is_tarfile(__cfgvalues['path']):
                __bck = CheckTar(__cfgvalues)
            # check a zip file
            elif __cfgvalues['type'] == 'archive' and is_zipfile(__cfgvalues['path']):
                __bck = CheckZip(__cfgvalues)
            ArchiveInfoMsg(__bck, __cfgvalues)
