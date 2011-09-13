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

from multiprocessing import Process, Queue
import subprocess
from os import linesep
import os.path

import functionaltests

EXE = './zozo'
OPTCONFIG = '-c'
OPTLOG = '-l'
OKMSG = 'OK'
KOMSG = 'KO - '

#class Test1_file_missing_in_tar_gz:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/file-missing-in-tar-gz'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file missing in' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test2_file_missing_in_tar_bz2:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/file-missing-in-tar-bz2'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file missing in' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test3_file_missing_in_zip:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/file-missing-in-zip'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file missing in' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test4_file_missing_in_tree:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/file-missing-in-tree'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file missing in' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test5_wrong_tar_gz_archive_mode:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-gz-archive-mode'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected mode' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test6_wrong_tar_bz2_archive_mode:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-mode'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected mode' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test7_wrong_zip_archive_mode:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-zip-archive-mode'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected mode' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test8_wrong_tar_gz_archive_uid:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-gz-archive-uid'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected uid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test9_wrong_tar_bz2_archive_uid:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-uid'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected uid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test10_wrong_zip_archive_uid:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-zip-archive-uid'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected uid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test11_wrong_tar_gz_archive_gid:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-gz-archive-gid'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected gid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test12_wrong_tar_bz2_archive_gid:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-gid'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected gid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test13_wrong_zip_archive_gid:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-zip-archive-gid'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected gid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test14_wrong_tar_gz_archive_md5_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-gz-archive-md5-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test15_wrong_tar_gz_archive_sha1_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-gz-archive-sha1-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test16_wrong_tar_gz_archive_sha224_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-gz-archive-sha224-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test17_wrong_tar_gz_archive_sha256_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-gz-archive-sha256-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test18_wrong_tar_gz_archive_sha384_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-gz-archive-sha384-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test19_wrong_tar_gz_archive_sha512_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-gz-archive-sha512-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test20_wrong_tar_bz2_archive_md5_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-md5-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test21_wrong_tar_bz2_archive_sha1_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-sha1-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test22_wrong_tar_bz2_archive_sha224_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-sha224-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test23_wrong_tar_bz2_archive_sha256_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-sha256-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test24_wrong_tar_bz2_archive_sha384_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-sha384-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test25_wrong_tar_bz2_archive_sha512_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-tar-bz2-archive-sha512-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test26_wrong_zip_archive_md5_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-zip-archive-md5-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test27_wrong_zip_archive_sha1_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-zip-archive-sha1-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test28_wrong_zip_archive_sha224_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-zip-archive-sha224-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test29_wrong_zip_archive_sha256_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-zip-archive-sha256-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test30_wrong_zip_archive_sha384_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-zip-archive-sha384-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test31_wrong_zip_archive_sha512_hash:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-zip-archive-sha512-hash'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test32_wrong_file_uid_in_tar_gz_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-uid-in-tar-gz-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected uid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test33_wrong_file_uid_in_tar_bz2_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-uid-in-tar-bz2-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected uid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test34_wrong_file_uid_in_tree:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-uid-in-tree'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected uid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test35_wrong_file_gid_in_tar_gz_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-gid-in-tar-gz-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected gid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test36_wrong_file_gid_in_tar_bz2_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-gid-in-tar-bz2-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected gid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test37_wrong_file_gid_in_tree:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-gid-in-tree'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected gid' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test38_unexpected_file_in_tar_gz_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/unexpected-file-in-tar-gz-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 unexpected file' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test39_unexpected_file_in_tar_bz2_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/unexpected-file-in-tar-bz2-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 unexpected file' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test40_unexpected_file_in_zip_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/unexpected-file-in-zip-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 unexpected file' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test41_unexpected_file_in_tree:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/unexpected-file-in-tree'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 unexpected file' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test42_wrong_file_md5_hash_in_tar_gz_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-md5-hash-in-tar-gz-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test43_wrong_file_sha1_hash_in_tar_gz_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha1-hash-in-tar-gz-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test44_wrong_file_sha224_hash_in_tar_gz_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha224-hash-in-tar-gz-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test45_wrong_file_sha256_hash_in_tar_gz_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha256-hash-in-tar-gz-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test46_wrong_file_sha384_hash_in_tar_gz_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha384-hash-in-tar-gz-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test47_wrong_file_sha512_hash_in_tar_gz_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha512-hash-in-tar-gz-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test48_wrong_file_md5_hash_in_tar_bz2_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-md5-hash-in-tar-bz2-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test49_wrong_file_sha1_hash_in_tar_bz2_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha1-hash-in-tar-bz2-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test50_wrong_file_sha224_hash_in_tar_bz2_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha224-hash-in-tar-bz2-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test51_wrong_file_sha256_hash_in_tar_bz2_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha256-hash-in-tar-bz2-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test52_wrong_file_sha384_hash_in_tar_bz2_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha384-hash-in-tar-bz2-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test53_wrong_file_sha512_hash_in_tar_bz2_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha512-hash-in-tar-bz2-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

#class Test54_wrong_file_md5_hash_in_zip_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-md5-hash-in-zip-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test55_wrong_file_sha1_hash_in_zip_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha1-hash-in-zip-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test56_wrong_file_sha224_hash_in_zip_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha224-hash-in-zip-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test57_wrong_file_sha256_hash_in_zip_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha256-hash-in-zip-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test58_wrong_file_sha384_hash_in_zip_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha384-hash-in-zip-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

#class Test59_wrong_file_sha512_hash_in_zip_archive:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha512-hash-in-zip-archive'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test60_wrong_file_md5_hash_in_tree:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-md5-hash-in-tree'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test61_wrong_file_sha1_hash_in_tree:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha1-hash-in-tree'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test62_wrong_file_sha224_hash_in_tree:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha224-hash-in-tree'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test63_wrong_file_sha256_hash_in_tree:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha256-hash-in-tree'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
#class Test64_wrong_file_sha384_hash_in_tree:
#    def __init__(self, q):
#        self.__queue = q
#        self.__testname = self.__class__.__name__
#        self.__testdir = 'functional-tests/wrong-file-sha384-hash-in-tree'
#        self.__resultfile = os.path.join(self.__testdir, 'a.out')
#        self.__main()
#
#    def __main(self):
#        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
#        if retcode != 0:
#            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
#        else:
#            with open(self.__resultfile, 'r') as __file:
#                if '1 file with unexpected hash' in __file.read():
#                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
#                else:
#                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))
#
class Test65_wrong_file_sha512_hash_in_tree:
    def __init__(self, q):
        self.__queue = q
        self.__testname = self.__class__.__name__
        self.__testdir = 'functional-tests/wrong-file-sha512-hash-in-tree'
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        self.__main()

    def __main(self):
        retcode = subprocess.call([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        if retcode != 0:
            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(retcode)))
        else:
            with open(self.__resultfile, 'r') as __file:
                if '1 file with unexpected hash' in __file.read():
                    self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
                else:
                    self.__queue.put('{} - {}value in result file not expected'.format(self.__testname, KOMSG))

def extract_key(key):
    return int(key.split('_')[0][4:])

if __name__ == '__main__':
    processes = []
    results = []
    q = Queue()

    for element in dir(functionaltests):
        if 'Test' in element:
            processes.append(Process(target=getattr(functionaltests, element), args=(q,)))
            processes[-1].start()
    for p in processes:
        results.append(q.get())
        p.join()
    # Only one print is beautiful
    print(linesep.join(sorted(results,key=functionaltests.extract_key)))
