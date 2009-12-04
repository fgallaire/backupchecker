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
