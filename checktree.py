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

# Check a file tree
"""Check a file tree"""

import os

from expectedfiles import ExpectedFiles
from checkarchive import CheckArchive

class CheckTree(CheckArchive):
    """Check a file tree"""

    def _main(self, _cfgvalues):
        """Main for CheckTree"""
        _data = []
        _data = ExpectedFiles(_cfgvalues['files_list']).data
        # Save the tree root to determine the relative path in the file tree
        __treeroot = os.path.split(_cfgvalues['path'])[0]
        for __dirpath, __dirnames, __filenames, in os.walk(_cfgvalues['path']):
            for __filename in __filenames:
                __filepath = os.path.join(__dirpath, __filename)
                __fileinfo = os.stat(__filepath)
                print('relpath:{}'.format(os.path.relpath(__filepath, _cfgvalues['path'])))
                _data = self._check_path(__fileinfo.st_size, os.path.relpath(
                        __filepath, __treeroot),
                            _data)
        self._missing_files = [_file['path'] for _file in _data]
