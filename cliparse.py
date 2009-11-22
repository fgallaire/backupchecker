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

# Retrieve the command line options
"""Retrieve the command line options"""

from optparse import OptionParser

class CliParse:
    """Retrieve the command line options"""

    def __init__(self):
        self._options = ()
        _parser = OptionParser(version="%prog 0.1")
        self.__define_options(_parser)

    def __define_options(self, _parser):
        """Define the options"""
        _parser.add_option("-c", "--configpath", dest="confpath",
            action="store", type="string",
            help="the path to the configurations",
            metavar="DIR")
        _parser.add_option("-i", "--input", dest="filename",
            action="store", type="string",
            help="the filename to check",
            metavar="FILE")
        _parser.add_option("-t", "--type", dest="type",
            action="store", type="string",
            help="type of the backup",
            metavar="FILE")
        _parser.add_option("-m", "--md5", dest="md5",
            action="store", type="string",
            help="in seconds the time between each order execution",
            metavar="MD5")
        self._options, _ = _parser.parse_args()

    def return_options(self):
        """Return the command line options"""
        return self._options
