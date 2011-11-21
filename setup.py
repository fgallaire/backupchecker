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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from distutils.core import setup
import platform
import sys

# Warn the user about the supported Python versions
if float(platform.python_version()[0:3]) < 3.2:
    print('You need at least Python 3.2 to use Brebis')
    sys.exit(1)

CLASSIFIERS = [
    'Intended Audience :: System Administrators',
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.2'
]

setup(name = 'brebis',
    version = '0.4',
    license = 'GNU GPL v3',
    description = 'automated backup checker',
    long_description = 'Brebis is a fully automated backup checker.',
    classifiers = CLASSIFIERS,
    author = 'Carl Chenet',
    author_email = 'chaica@brebisproject.org',
    url = 'http://www.brebisproject.org',
    download_url = 'http://www.brebisproject.org',
    packages = ['brebis', 'brebis.checkbackups', 'brebis.generatelist'],
    scripts = ['scripts/brebis']
)
