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

# Generate the information message about an archive
'''Generate the information message about an archive'''

import logging

class ArchiveInfoMsg(object):
    '''Generate the information message about an archive'''

    def __init__(self, __bck, __cfgvalues):
        self.__main(__bck, __cfgvalues)

    def __main(self, __bck, __cfgvalues):
        '''The main for the ArchiveInfoMsg class'''
        if __cfgvalues['type'] == 'archive' or __cfgvalues['type'] == 'tree':
            self.__missing_files(__bck.missing_files, __cfgvalues['path'])
            self.__classify_differences(__bck, __cfgvalues['path'])

    def __missing_files(self, __missing, __archivepath):
        '''Warn about the missing files in an archive'''
        if __missing:
            __msg= 'file'
            if len(__missing) > 1:
                __msg = 'files'
            logging.warn('{} {} missing in {}: '.format(
                len(__missing), __msg, __archivepath))
            for __path in __missing:
                logging.warn('{}'.format(__path))

    def __classify_differences(self, __bck, __archivepath):
        '''Report differences between expected files and files in the
        archive
        '''
        if __bck.missing_equality:
            __topic = '{} {} with unexpected size in {}: '
            self.__log_differences(
                __bck.missing_equality, __archivepath, __topic)
        if __bck.missing_smaller_than:
            __topic = '{} {} bigger than expected in {}: '
            self.__log_differences(
                __bck.missing_smaller_than, __archivepath,
                    __topic, 'smaller than')
        if __bck.missing_bigger_than:
            __topic = '{} {} smaller than expected in {}: '
            self.__log_differences(
                __bck.missing_bigger_than, __archivepath,
                    __topic, 'bigger than')

    def __log_differences(self, __files, __archivepath, __topic, __qty=''):
        '''Log the differences between the expected files and the files
        in the archive
        '''
        __fileword = 'file'
        if len(__files) > 1:
            __fileword = 'files'
        logging.warn(__topic.format(len(__files), __fileword, __archivepath))
        if __qty:
            for __file in __files:
                logging.warn('{} size is {}. Should have been {} {}.'.format(
                    __file['path'], __file['size'], __qty, __file['expected']))
        else:
            for __file in __files:
                logging.warn('{} size is {}. Should have been {}.'.format(
                    __file['path'], __file['size'], __file['expected']))
