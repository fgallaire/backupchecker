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
'''Retrieve the command line options'''

import logging
from optparse import OptionParser
import os
import sys

from applogger import AppLogger

class CliParse:
    '''Retrieve the command line options'''

    def __init__(self):
        self._options = ()
        __parser = OptionParser(version="%prog 0.1")
        self.__define_options(__parser)

    def __define_options(self, __parser):
        '''Define the options'''
        __parser.add_option('-c', '--configpath', dest='confpath',
            action='store', type='string',
            default=os.getcwd(),
            help='the path to the configurations',
            metavar='DIR')
        __parser.add_option('-l', '--log', dest='logfile',
            action='store', type='string',
            default=os.path.join(os.getcwd(), 'a.out'),
            help='the log file',
            metavar='FILE')
        __parser.add_option('-t', '--type', dest='type',
            action='store', type='string',
            help='type of the backup',
            metavar='FILE')
        __parser.add_option('--hashfile', dest='hashfile',
            action='store', type='string',
            help='the file containing the hashes',
            metavar='FILE')
        for __hashtype in ['md5', 'sha1', 'sha224','sha256','sha384','sha512']:
            __parser.add_option('--{}'.format(__hashtype), dest='hashtype',
                action='store_const', const='{}'.format(__hashtype),
                help='use the {} hash algorithm type'.format(__hashtype))
        __options, _ = __parser.parse_args()
        self.__verify_options(__options)

    def __verify_options(self, __options):
        '''Verify the options given on the command line'''
        # Check the logfile
        __logdir = os.path.split(__options.logfile)[0]
        if __logdir and not os.path.exists(__logdir):
            print('split:{}'.format(os.path.split(__options.logfile)[0]))
            print('The directory where to write the log file does not exist')
            sys.exit(1)
        __options.logfile = os.path.abspath(__options.logfile)
        # Configure the logger
        AppLogger(__options.logfile)
        # Check the configuration directory
        if not os.path.exists(__options.confpath):
            logging.info('The configuration directory does not exist')
            sys.exit(1)
        __options.confpath = os.path.abspath(__options.confpath)
        # Check if hashfile and hashtype are both defined
        if __options.hashtype and __options.hashfile:
            # Check the hash file path
            if not os.path.exists(__options.hashfile):
                print('The hash file does not exist')
                sys.exit(1)
        __hashwarning = 'You should provide both hash type and hash file'
        elif __options.hashtype and not __options.hashfile:
            print(__hashwarning)
            sys.exit(1)
        elif __options.hashfile and not __options.hashtype:
            print(__hashwarning)
            sys.exit(1)
        self.__options = __options

    @property
    def options(self):
        '''Return the command line options'''
        return self.__options
