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

class CheckTar(object):
    """Check a tar archive"""

    def __init__(self, _cfgvalues):
        self._missing_files = []
        self._missing_equality = []
        self._missing_biggerthan = []
        self._missing_smallerthan = []
        self.__main(_cfgvalues)

    def __main(self, _cfgvalues):
        """Main for CheckTar"""
        _data = []
        try:
            _data = ExpectedFiles(_cfgvalues['files_list']).data
            _tar = tarfile.open(_cfgvalues['path'], 'r')
            for _tarinfo in _tar:
                _data = self.__check_path(_tarinfo, _data)
            self._missing_files = [_file['path'] for _file in _data]
        except tarfile.TarError as _msg:
            print(_msg)
        finally:
            _tar.close()

    def __check_path(self, _tarinfo, _data):
        """Check if the expected path exists in the tar file"""
        print('_data:{}'.format(_data))
        for _ind, _file in enumerate(_data):
            if _tarinfo.name == _file['path']:
                if 'equals' in _file:
                    self.__check_equality(_tarinfo, _file)
                elif 'biggerthan' in _file:
                    self.__check_bigger_than(_tarinfo, _file)
                elif 'smallerthan' in _file:
                    self.__check_smaller_than(_tarinfo, _file)
                del(_data[_ind])
        return _data

    def __check_equality(self, _bck, _file):
        """Check if the file in the archive respects the expected equality"""
        if _bck.size != _file['equals']:
            self.missing_equality.append({'path': _bck.name,
                'size': _bck.size, 'expected': _file['equals']})

    def __check_bigger_than(self, _bck, _file):
        """Check if the file in the archive respects the bigger than parameter"""
        if _bck.size < _file['biggerthan']:
            self.missing_biggerthan.append({'path': _bck.name,
                'size': _bck.size, 'expected': _file['biggerthan']})

    def __check_smaller_than(self, _bck, _file):
        """check if the file in the archive respects the smaller than parameter"""
        if _bck.size > _file['smallerthan']:
            self.missing_smallerthan.append({'path': _bck.name,
                'size': _bck.size, 'expected': _file['smallerthan']})

    @property
    def missing_equality(self):
        """A list containing the paths of the files missing the equality parameters in the archive"""
        return self._missing_equality

    @property
    def missing_files(self):
        """A list containing the paths of the missing files in the archive"""
        return self._missing_files

    @property
    def missing_biggerthan(self):
        """A list containing the path and the size of the files missing the bigger than parameter in the archive"""
        return self._missing_biggerthan

    @property
    def missing_smallerthan(self):
        """A list containing the path and the size of the files missing the smaller than parameter in the archive"""
        return self._missing_smallerthan
