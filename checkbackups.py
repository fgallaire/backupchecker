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

# Check the given backups
"""Check the given backups"""

from tarfile import is_tarfile

from checktar import CheckTar

class CheckBackups(object):
    """The main class for Brebis"""

    def __init__(self, _confs):
        self.__main(_confs)

    def __main(self, _confs):
        _cfgsets = _confs.values()
        for _cfgvalues in _cfgsets:
            if is_tarfile(_cfgvalues['path']):
                CheckTar(_cfgvalues)
                
