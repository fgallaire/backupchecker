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
"""Check the given backups"""

import logging
from tarfile import is_tarfile
from zipfile import is_zipfile

from checktar import CheckTar
from checkzip import CheckZip

class CheckBackups(object):
    """The main class for Brebis"""

    def __init__(self, _confs):
        self.__main(_confs)

    def __main(self, _confs):
        """Main for CheckBackups"""
        _cfgsets = _confs.values()
        for _cfgvalues in _cfgsets:
            # check a tar file
            if is_tarfile(_cfgvalues['path']):
                _bck = CheckTar(_cfgvalues)
                self.__compute_result(_bck, _cfgvalues)
            # check a zip file
            if is_zipfile(_cfgvalues['path']):
                _bck = CheckZip(_cfgvalues)
                self.__compute_result(_bck, _cfgvalues)
                
    def __compute_result(self, _bck, _cfgvalues):
        """Launch action depending on the result and type of the backup"""
        if _cfgvalues['type'] == 'archive':
            self.__missing_files(_bck.missing_files, _cfgvalues['path'])
            self.__classify_differences(_bck, _cfgvalues['path'])

    def __missing_files(self, _missing, _archivepath):
        """Warn about the missing files in an archive"""
        if _missing:
            _msg= 'file'
            if len(_missing) > 1:
                _msg = 'files'
            logging.warn('{} {} missing in {}: '.format(len(_missing), _msg, _archivepath))
            for _path in _missing:
                logging.warn('{}'.format(_path))

    def __classify_differences(self, _bck, _archivepath):
        """Report differences between expected files and files in the archive"""
        if _bck.missing_equality:
            _topic = '{} {} with unexpected size in {}: '
            self.__log_differences(_bck.missing_equality, _archivepath, _topic)
        if _bck.missing_smaller_than:
            _topic = '{} {} bigger than expected in {}: '
            self.__log_differences(_bck.missing_smaller_than, _archivepath, _topic)
        if _bck.missing_bigger_than:
            _topic = '{} {} smaller than expected in {}: '
            self.__log_differences(_bck.missing_bigger_than, _archivepath, _topic)

    def __log_differences(self, _files, _archivepath, _topic):
        """Log the differences between the expected files and the files in the archive"""
        _fileword = 'file'
        if len(_files) > 1:
            _fileword = 'files'
        logging.warn(_topic.format(len(_files), _fileword, _archivepath))
        for _file in _files:
            logging.warn('{} size is {}. Should have been {}.'.format(_file['path'], _file['size'], _file['expected']))
