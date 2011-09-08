#!/usr/bin/python3.2
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

import subprocess
import os.path

class Test1_file_missing_in_tar_gz:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/file-missing-in-tar-gz'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call(['./zozo', '-c', self.__testdir, '-l', self.__resultfile])
        if retcode != 0:
            print('{} KO - return code:{}'.format(self.__testname, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file missing in' in __file.read():
                    print('{} OK'.format(self.__testname))
                else:
                    print('{} KO - value in result file not expected'.format(self.__testname))

class Test2_file_missing_in_tar_bz2:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/file-missing-in-tar-bz2'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call(['./zozo', '-c', self.__testdir, '-l', self.__resultfile])
        if retcode != 0:
            print('{} KO - return code:{}'.format(self.__testname, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file missing in' in __file.read():
                    print('{} OK'.format(self.__testname))
                else:
                    print('{} KO - value in result file not expected'.format(self.__testname))

class Test3_file_missing_in_zip:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/file-missing-in-zip'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call(['./zozo', '-c', self.__testdir, '-l', self.__resultfile])
        if retcode != 0:
            print('{} KO - return code:{}'.format(self.__testname, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file missing in' in __file.read():
                    print('{} OK'.format(self.__testname))
                else:
                    print('{} KO - value in result file not expected'.format(self.__testname))


if __name__ == '__main__':
    Test1_file_missing_in_tar_gz()
    Test2_file_missing_in_tar_bz2()
    Test3_file_missing_in_zip()
