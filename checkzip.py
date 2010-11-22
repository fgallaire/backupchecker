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

# Check a zip archive
'''Check a zip archive'''

import sys
import zipfile

from expectedfiles import ExpectedFiles
from checkarchive import CheckArchive

class CheckZip(CheckArchive):
    '''Check a zip archive'''

    def _main(self, _cfgvalues):
        '''Main for CheckZip'''
        _crcerror = ''
        _data = []
        try:
            _data= ExpectedFiles(_cfgvalues['files_list']).data
            self._zip = zipfile.ZipFile(_cfgvalues['path'], 'r', allowZip64=True)
            _crcerror = self._zip.testzip()
            if _crcerror:
                logging.warn('{} has at least a file corrupted:{}'.format(_cfgvalues['path'], _crcerror))
            else:
                _zipinfo = self._zip.infolist()
                for _fileinfo in _zipinfo:
                    __arcinfo = {'path': _fileinfo.filename, 'size': _fileinfo.file_size}
                    _data = self._check_path(__arcinfo, _data)
                self._missing_files = [_file['path'] for _file in _data]
        except zipfile.BadZipfile as _msg:
            print(_msg)
        finally:
            self._zip.close()

    def _extract_stored_file(self, __arcfilepath):
        '''Extract a file from the archive and return a file object'''
        __file = self._zip.open(__arcfilepath, 'r')
        return __file
