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
from checkdb import CheckDb
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
                #self.__compute_result(__bck, __cfgvalues)
                ArchiveInfoMsg(__bck, __cfgvalues)
            elif __cfgvalues['type'] == 'db':
                CheckDb(__cfgvalues)
            # check a tar file
            elif __cfgvalues['type'] == 'archive' and is_tarfile(__cfgvalues['path']):
                __bck = CheckTar(__cfgvalues)
                #self.__compute_result(__bck, __cfgvalues)
                ArchiveInfoMsg(__bck, __cfgvalues)
            # check a zip file
            elif __cfgvalues['type'] == 'archive' and is_zipfile(__cfgvalues['path']):
                __bck = CheckZip(__cfgvalues)
                #self.__compute_result(__bck, _c_fgvalues)
                ArchiveInfoMsg(__bck, __cfgvalues)
                
#    def __compute_result(self, __bck, __cfgvalues):
#        '''Launch action depending on the result and type of the backup'''
#        if __cfgvalues['type'] == 'archive' or __cfgvalues['type'] == 'tree':
#            self.__missing_files(__bck.missing_files, __cfgvalues['path'])
#            self.__classify_differences(__bck, __cfgvalues['path'])
#
#    def __missing_files(self, __missing, __archivepath):
#        '''Warn about the missing files in an archive'''
#        if __missing:
#            __msg= 'file'
#            if len(__missing) > 1:
#                __msg = 'files'
#            logging.warn('{} {} missing in {}: '.format(len(__missing), __msg, __archivepath))
#            for __path in __missing:
#                logging.warn('{}'.format(__path))
#
#    def __classify_differences(self, __bck, __archivepath):
#        '''Report differences between expected files and files in the archive'''
#        if __bck.missing_equality:
#            __topic = '{} {} with unexpected size in {}: '
#            self.__log_differences(__bck.missing_equality, __archivepath, __topic)
#        if __bck.missing_smaller_than:
#            __topic = '{} {} bigger than expected in {}: '
#            self.__log_differences(__bck.missing_smaller_than, __archivepath, __topic)
#        if __bck.missing_bigger_than:
#            __topic = '{} {} smaller than expected in {}: '
#            self.__log_differences(__bck.missing_bigger_than, __archivepath, __topic)
#
#    def __log_differences(self, __files, __archivepath, __topic):
#        '''Log the differences between the expected files and the files in the archive'''
#        __fileword = 'file'
#        if len(__files) > 1:
#            __fileword = 'files'
#        logging.warn(__topic.format(len(__files), __fileword, __archivepath))
#        for __file in __files:
#            logging.warn('{} size is {}. Should have been {}.'.format(__file['path'], __file['size'], __file['expected']))
