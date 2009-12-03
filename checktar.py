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

# Check a tar archive
"""Check a tar archive"""

import sys
import tarfile

from expectedfiles import ExpectedFiles
from checkarchive import CheckArchive

class CheckTar(CheckArchive):
    """Check a tar archive"""

    def _main(self, _cfgvalues):
        """Main for CheckTar"""
        _data = []
        try:
            _data = ExpectedFiles(_cfgvalues['files_list']).data
            _tar = tarfile.open(_cfgvalues['path'], 'r')
            for _tarinfo in _tar:
                _data = self._check_path(_tarinfo.size, _tarinfo.name, _data)
            self._missing_files = [_file['path'] for _file in _data]
        except tarfile.TarError as _msg:
            print(_msg)
        finally:
            _tar.close()

#    def __check_path(self, _tarinfo, _data):
#        """Check if the expected path exists in the tar file"""
#        for _ind, _file in enumerate(_data):
#            if _tarinfo.name == _file['path']:
#                self.__compare_sizes(_tarinfo, _file)
#                del(_data[_ind])
#        return _data
#
#    def __compare_sizes(self, _tar, _file):
#        """Compare the sizes of the files in the archive and the expected files"""
#        if 'equals' in _file and _tar.size != _file['equals']:
#            self.missing_equality.append({'path': _tar.name,
#                'size': _tar.size, 'expected': _file['equals']})
#        elif 'biggerthan' in _file and _tar.size < _file['biggerthan']:
#            self.missing_bigger_than.append({'path': _tar.name,
#                'size': _tar.size, 'expected': _file['biggerthan']})
#        elif 'smallerthan' in _file and _tar.size > _file['smallerthan']:
#            self.missing_smaller_than.append({'path': _tar.name,
#                'size': _tar.size, 'expected': _file['smallerthan']})
#        
