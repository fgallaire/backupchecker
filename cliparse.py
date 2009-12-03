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
        _parser.add_option('-c', '--configpath', dest='confpath',
            action='store', type='string',
            help='the path to the configurations',
            metavar='DIR')
        _parser.add_option('-l', '--log', dest='logfile',
            action='store', type='string',
            help='the Brebis log file',
            metavar='FILE')
        _parser.add_option('-t', '--type', dest='type',
            action='store', type='string',
            help='type of the backup',
            metavar='FILE')
        _parser.add_option('--hashfile', dest='hashfile',
            action='store', type='string',
            help='the file containing the hashes',
            metavar='FILE')
        for _hashtype in ['md5', 'sha1', 'sha224','sha256','sha384','sha512']:
            _parser.add_option('--{}'.format(_hashtype), dest='hashtype',
                action='store_const', const='{}'.format(_hashtype),
                help='use the {} hash type'.format(_hashtype))
        _options, _ = _parser.parse_args()
        self.__verify(_options)

    def __verify(self, _options):
        """Verify options"""
        # Check the logfile
        _logdir = os.path.split(_options.logfile)[0]
        if _logdir and not os.path.exists(_logdir):
            print('split:{}'.format(os.path.split(_options.logfile)[0]))
            print('The directory where to write the log file does not exist')
            sys.exit(1)
        # Configure the logger
        BrebisLogger(_options.logfile)
        # Check the configuration directory
        if not os.path.exists(_options.confpath):
            logging.info('The configuration directory does not exist')
            sys.exit(1)
        # Check if hashfile and hashtype are both defined
        if _options.hashtype and _options.hashfile:
            # Check the hash file path
            if not os.path.exists(_options.hashfile):
                print('The hash file does not exist')
                sys.exit(1)
        elif _options.hashtype and not _options.hashfile:
            print('A hash algorithm is defined but you do not provide the file with the hash sums')
            sys.exit(1)
        elif _options.hashfile and not _options.hashtype:
            print('A file with the hash sums are given but you do not provide the hash algorithm you wish to use')
            sys.exit(1)
        self._options = _options

    @property
    def options(self):
        """Return the command line options"""
        return self._options
