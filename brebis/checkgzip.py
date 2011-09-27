# -*- coding: utf-8 -*-
# Copyright © 2011 Carl Chenet <chaica@ohmytux.com>
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

# Check a gzip archive
'''Check a gzip archive'''

import sys
import logging
import os.path

from brebis.checkarchive import CheckArchive
from brebis.expectedvalues import ExpectedValues

class CheckGzip(CheckArchive):
    '''Check a tar archive'''

    def _main(self, _cfgvalues):
        '''Main for Checkgzip'''
        _data = []
        _data, __arcdata = ExpectedValues(_cfgvalues['files_list']).data
        #########################
        # Test the archive itself
        #########################
        self._archive_checks(__arcdata, _cfgvalues['path'])
        ###############################
        # Test the file in the archive
        ###############################
        if _data:
            self._gzip = open(_cfgvalues['path'], 'rb')
            __filesize = self.__extract_size(self._gzip)
            __arcinfo = {'path': os.path.split(_cfgvalues['path'])[-1].rstrip('.gz'),
                            'size': __filesize}
            _data = self._check_path(__arcinfo, _data)

    def __extract_size(self, __binary):
        '''Extract the size of the uncompressed file inside the archive -
        4 last bytes of the archive
        '''
        return int.from_bytes(__binary.read(__binary.seek(-4, 2)), 'little')
