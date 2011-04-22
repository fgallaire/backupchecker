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

from setuptools import setup

CLASSIFIERS = [
    'Intended Audience :: System Administrators',
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.2'
]



setup(name = 'brebis',
    version = '0.1',
    license = 'GNU GPL v3',
    description = 'automated backup checker',
    long_description = 'Brebis is a fully automated backup checker.',
    classifiers = CLASSIFIERS,
    author = 'Carl Chenet',
    author_email = 'chaica@brebis-project.org',
    url = 'http://www.brebis-project.org',
    download_url = 'http://www.brebis-project.org',
    packages = ['brebis'],
    entry_points=dict(console_scripts=['brebis=brebis:main']),
    install_requires=['distribute']
)
