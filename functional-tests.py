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

EXE = './zozo'
OPTCONFIG = '-c'
OPTLOG = '-l'
OKMSG = 'OK'
KOMSG = 'KO - '

class Test1_file_missing_in_tar_gz:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/file-missing-in-tar-gz'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file missing in' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

class Test2_file_missing_in_tar_bz2:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/file-missing-in-tar-bz2'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file missing in' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

class Test3_file_missing_in_zip:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/file-missing-in-zip'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file missing in' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

class Test4_file_missing_in_tree:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/file-missing-in-tree'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file missing in' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

class Test5_wrong_tar_gz_archive_mode:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/wrong-tar-gz-archive-mode'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file with unexpected mode' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

class Test6_wrong_tar_bz2_archive_mode:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-mode'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file with unexpected mode' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

class Test7_wrong_zip_archive_mode:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/wrong-zip-archive-mode'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file with unexpected mode' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

class Test8_wrong_tar_gz_archive_uid:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/wrong-tar-gz-archive-uid'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file with unexpected uid' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

class Test9_wrong_tar_bz2_archive_uid:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-uid'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file with unexpected uid' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

class Test10_wrong_zip_archive_uid:
    def __init__(self):
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/wrong-zip-archive-uid'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            print('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file with unexpected uid' in __file.read():
                    print('{} - {}'.format(self.__testname, OKMSG))
                else:
                    print('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

if __name__ == '__main__':
    Test1_file_missing_in_tar_gz()
    Test2_file_missing_in_tar_bz2()
    Test3_file_missing_in_zip()
    Test4_file_missing_in_tree()
    Test5_wrong_tar_gz_archive_mode()
    Test6_wrong_tar_bz2_archive_mode()
    Test7_wrong_zip_archive_mode()
    Test8_wrong_tar_gz_archive_uid()
    Test9_wrong_tar_bz2_archive_uid()
    Test10_wrong_zip_archive_uid()
