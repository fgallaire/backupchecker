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

# Check an archive
'''Check an archive'''

class CheckArchive(object):
    '''Check an archive'''

    def __init__(self, _cfgvalues):
        self._missing_files = []
        self._missing_equality = []
        self._missing_bigger_than = []
        self._missing_smaller_than = []
        self._main(_cfgvalues)

    def _check_path(self, _arcsize, _arcname, _data):
        '''Check if the expected path exists in the archive'''
        for _ind, _file in enumerate(_data):
            if _arcname == _file['path']:
                self._compare_sizes(_arcsize, _arcname, _file)
                del(_data[_ind])
        return _data

    def _compare_sizes(self, _arcsize, _arcname, _file):
        '''Compare the sizes of the files in the archive and the expected files'''
        if 'equals' in _file and _arcsize != _file['equals']:
            self.missing_equality.append({'path': _arcname,
                'size': _arcsize, 'expected': _file['equals']})
        elif 'biggerthan' in _file and _arcsize < _file['biggerthan']:
            self.missing_bigger_than.append({'path': _arcname,
                'size': _arcsize, 'expected': _file['biggerthan']})
        elif 'smallerthan' in _file and _arcsize > _file['smallerthan']:
            self.missing_smaller_than.append({'path': _arcname,
                'size': _arcsize, 'expected': _file['smallerthan']})
        
    @property
    def missing_equality(self):
        '''A list containing the paths of the files missing the equality parameters in the archive'''
        return self._missing_equality

    @property
    def missing_files(self):
        '''A list containing the paths of the missing files in the archive'''
        return self._missing_files

    @property
    def missing_bigger_than(self):
        '''A list containing the path and the size of the files missing the bigger than parameter in the archive'''
        return self._missing_bigger_than

    @property
    def missing_smaller_than(self):
        '''A list containing the path and the size of the files missing the smaller than parameter in the archive'''
        return self._missing_smaller_than
