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
import sys
import os
import logging

from brebislogger import BrebisLogger

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
        _parser.add_option("-l", "--log", dest="logfile",
            action="store", type="string",
            help="the Brebis log file",
            metavar="FILE")
        _parser.add_option("-t", "--type", dest="type",
            action="store", type="string",
            help="type of the backup",
            metavar="FILE")
        _parser.add_option("--hashfile", dest="hashfile",
            action="store", type="string",
            help="the file containing the hashes",
            metavar="FILE")
        _parser.add_option("--md5", dest="hashtype",
            action="store_const", const="md5",
            help="use the MD5 hash type")
        _parser.add_option("--sha1", dest="hashtype",
            action="store_const", const="sha1",
            help="use the SHA1 hash type")
        _options, _ = _parser.parse_args()
        self.__verify(_options)

    def __verify(self, _options):
        """Verify options"""
        _logdir = os.path.split(_options.logfile)[0]
        if _logdir and not os.path.exists(_logdir):
            print('split:{}'.format(os.path.split(_options.logfile)[0]))
            print('The directory where to write the log file does not exist')
            sys.exit(1)
        BrebisLogger(_options.logfile)
        if not os.path.exists(_options.confpath):
            logging.info('The configuration directory does not exist')
            sys.exit(1)
        self._options = _options

    @property
    def options(self):
        """Return the command line options"""
        return self._options
