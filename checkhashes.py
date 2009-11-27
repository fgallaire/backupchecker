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

# Check the files hashes
"""Check the files hashes"""

import hashlib
import logging
import os.path
import sys

class CheckHashes(object):
    """Check the files hashes"""

    def __init__(self, _hashfile, _hashtype, _confs):
        self._confs = _confs
        self.__main(_hashfile, _hashtype, _confs)

    def __main(self, _hashfile, _hashtype, _confs):
        """Main for the CheckHashes class"""
        _hashinfo = self.__extract_hashinfo(_hashfile)
        self.__check_hashes(_hashtype, _confs, _hashinfo)

    def __check_hashes(self, _hashtype, _confs, _hashinfo):
        """check the hash of the backups"""
        try:
            _confstoremove = []
            for _conf in _confs:
                _bckname = os.path.split(_confs[_conf]['path'])[-1]
                if _bckname in _hashinfo:
                    with open(_confs[_conf]['path'], 'rb') as _file:
                        _res = getattr(hashlib, _hashtype)(_file.read()).hexdigest()
                        if _res != _hashinfo[_bckname]:
                            logging.info('The {} checksum mismatched'.format(_confs[_conf]['path']))
                            _confstoremove.append(_conf)
            for _conf in _confstoremove:
                del(self._confs[_conf])
        except (OSError, IOError) as _msg:
            logging.info(_msg)

    def __extract_hashinfo(self, _hashfile):
        """Extract the info about hashed files"""
        _hashinfo = {}
        try:
            with open(_hashfile) as _files:
                for _file in _files:
                    _data = _file.split()
                    if len(_data) != 2:
                        logging.info('{} has not a hash file valid format - should be only two arguments by line'.format(_hashfile))
                        sys.exit(1)
                    else:
                        _hashinfo[_data[-1]] = _data[0]
        except (OSError, IOError) as _msg:
            print(_msg)
            sys.exit(1)
        return _hashinfo
        
    @property
    def confs(self):
        """Returne the configurations minus the ones containing a corrupted file"""
        return self._confs
