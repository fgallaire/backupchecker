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

class CheckTar(object):
    """Check a tar archive"""

    def __init__(self, _cfgvalues):
        self.__main(_cfgvalues)

    def __main(self, _cfgvalues):
        """Main for CheckTar"""
        _found = False
        try:
            _tar =  tarfile.open(_cfgvalues['path'], 'r')
            for _tarinfo in _tar:
                if _tarinfo.name == _cfgvalues['expected_file']:
                    _found = True
                    print('The expected file was found')
            if not _found:
                print('The expected file was not found in the archive')
        except tarfile.CompressionError as _msg:
            print(_msg)
        finally:
            _tar.close()
