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

import tarfile
import sys

from expectedfiles import ExpectedFiles

class CheckTar(object):
    """Check a tar archive"""

    def __init__(self, _cfgvalues):
        self.__main(_cfgvalues)

    def __main(self, _cfgvalues):
        """Main for CheckTar"""
        _paths = []
        try:
            _paths = ExpectedFiles(_cfgvalues['files_list']).paths
            _tar = tarfile.open(_cfgvalues['path'], 'r')
            for _tarinfo in _tar:
                for _ind, _file in enumerate(_paths):
                    if _tarinfo.name == _file:
                        del(_paths[_ind])
            self._missingfiles = _paths
        except tarfile.TarError as _msg:
            print(_msg)
        finally:
            _tar.close()

    @property
    def missing_files(self):
        return self._missingfiles
