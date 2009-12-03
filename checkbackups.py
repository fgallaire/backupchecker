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
            self.__missing_equality(_bck.missing_equality, _cfgvalues['path'])
            self.__smaller_than_expected_files(_bck.missing_biggerthan, _cfgvalues['path'])
            self.__bigger_than_expected_files(_bck.missing_smallerthan, _cfgvalues['path'])

    def __missing_files(self, _missing, _archivepath):
        """Warn about the missing files in an archive"""
        if _missing:
            _msg= 'file'
            if len(_missing) > 1:
                _msg = 'files'
            logging.info('{} {} missing in {}: '.format(len(_missing), _msg, _archivepath))
            for _path in _missing:
                logging.info('{}'.format(_path))

    def __smaller_than_expected_files(self, _smaller, _archivepath):
        """Warn about the smaller than expected files in the archive"""
        if _smaller:
            _msg= 'file'
            if len(_smaller) > 1:
                _msg = 'files'
            logging.info('{} {} smaller than expected in {}: '.format(len(_smaller), _msg, _archivepath))
            for _file in _smaller:
                logging.info('{} size is {}. Should have been {}.'.format(_file['path'], _file['size'], _file['expected']))
        
    def __bigger_than_expected_files(self, _bigger, _archivepath):
        """Warn about the bigger than expected files in the archive"""
        if _bigger:
            _msg= 'file'
            if len(_bigger) > 1:
                _msg = 'files'
            logging.info('{} {} bigger than expected in {}: '.format(len(_bigger), _msg, _archivepath))
            for _file in _bigger:
                logging.info('{} size is {}. Should have been {}.'.format(_file['path'], _file['size'], _file['expected']))
        
    def __missing_equality(self, _equality, _archivepath):
        """Warn about the size equality between the expected files and the files in the archive"""
        if _equality:
            _msg= 'file'
            if len(_equality) > 1:
                _msg = 'files'
            logging.info('{} {} with unexpected size in {}: '.format(len(_equality), _msg, _archivepath))
            for _file in _equality:
                logging.info('{} size is {}. Should have been {}.'.format(_file['path'], _file['size'], _file['expected']))
