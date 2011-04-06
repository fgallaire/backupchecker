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

from expectedvalues import ExpectedValues
from checkarchive import CheckArchive
import checkhashes

class CheckZip(CheckArchive):
    '''Check a zip archive'''

    def _main(self, _cfgvalues):
        '''Main for CheckZip'''
        _crcerror = ''
        _data = []
        _data, __arcdata = ExpectedValues(_cfgvalues['files_list']).data
        #########################
        # Test the archive itself
        #########################
        if __arcdata:
            if 'equals' in __arcdata or 'biggerthan' in __arcdata or 'smallerthan' in __arcdata:
                __arcsize = self._find_archive_size(_cfgvalues['path'])
                self._compare_sizes(__arcsize, _cfgvalues['path'], __arcdata)
            # archive hash
            if 'hash' in __arcdata:
                with open(_cfgvalues['path'], 'rb') as __archive:
                    __archash = checkhashes.get_hash(__archive, __arcdata['hash']['hashtype'])
                    self._report_hash(_cfgvalues['path'], __arcdata['hash']['hashvalue'], __archash)
        ###############################
        # Test the files in the archive
        ###############################
        if _data:
            try:
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
