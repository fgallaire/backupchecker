#!/home/chaica/progra/python/Python-3.3.0b1/python
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

import hashlib
from multiprocessing import Process, Queue
from os import linesep, environ
import subprocess
import os.path
import sys

import functionaltests

EXE = './brebis.py'
OPTCONFIG = '-c'
OPTLOG = '-l'
OPTGEN = '-g'
OKMSG = 'ok'
KOMSG = 'ko - '
PYTHONEXE =''
ABSPATH = ''

# To correctly use the tests with buildbot
if 'PYTHONEXE' in environ:
    PYTHONEXE = environ['PYTHONEXE']
    ABSPATH = environ['PWD']

class Main:
    '''Main of all the Test* classes'''
    def _main(self, __condition):
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, self._testdir, OPTLOG, self._resultfile])
        else:
            __retcode = subprocess.call([EXE, OPTCONFIG, self._testdir, OPTLOG, self._resultfile])
        if __retcode != 0:
            self._queue.put('{} - {}return code:{}'.format(self._testname, KOMSG, str(__retcode)))
        else:
            with open(self._resultfile, 'r') as __file:
                if __condition in __file.read():
                    self._queue.put('{} - {}'.format(self._testname, OKMSG))
                else:
                    self._queue.put('{} - {}value in result file not expected'.format(self._testname, KOMSG))

class MainGenerateParse:
    '''Main of all the Test*GenerateParse classes'''
    def _main(self, __condition):
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, self._testdir, OPTLOG, self._resultfile])
        else:
            __retcode = subprocess.call([EXE, OPTCONFIG, self._testdir, OPTLOG, self._resultfile])
        if __retcode != 0:
            self._queue.put('{} - {}return code:{}'.format(self._testname, KOMSG, str(__retcode)))
        else:
            with open(self._resultfile, 'r') as __file:
                if '' == __file.read():
                    self._queue.put('{} - {}'.format(self._testname, OKMSG))
                else:
                    self._queue.put('{} - {}value in result file not expected'.format(self._testname, KOMSG))

class Test_file_missing_in_tar(Main):
    '''Test if a file is missing in a tar archive'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-tar')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test_file_missing_in_tar_gz(Main):
    '''Test if a file is missing in a tar.gz archive'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-tar-gz')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test_file_missing_in_tar_bz2(Main):
    '''Test if a file is missing in a tar.bz2 archive'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-tar-bz2')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test_file_missing_in_tar_xz(Main):
    '''Test if a file is missing in a tar.xz archive'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-tar-xz')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test_file_missing_in_gzip(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-gzip')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test_file_missing_in_zip(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-zip')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test_file_missing_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test_wrong_tar_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_tar_gz_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_tar_bz2_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_gzip_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_zip_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_tar_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-archive-uid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_tar_gz_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-uid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_tar_bz2_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-uid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_zip_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-uid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_gz_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-uid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_tar_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_tar_gz_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_tar_bz2_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_gzip_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_zip_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_tar_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-archive-sha1-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_gz_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_gz_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha1-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_gz_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_gz_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_gz_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_gz_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_bz2_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_bz2_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha1-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_bz2_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_bz2_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_bz2_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_bz2_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_gzip_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_gzip_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-sha1-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_gzip_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_gzip_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_gzip_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_gzip_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_bzip2_archive_md5_hash(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-bz2-archive-md5-hash')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected hash')

class Test_wrong_bzip2_archive_sha1_hash(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-bz2-archive-sha1-hash')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected hash')

class Test_wrong_bzip2_archive_sha224_hash(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-bz2-archive-sha224-hash')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected hash')

class Test_wrong_bzip2_archive_sha256_hash(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-bz2-archive-sha256-hash')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected hash')

class Test_wrong_bzip2_archive_sha384_hash(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-bz2-archive-sha384-hash')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected hash')

class Test_wrong_bzip2_archive_sha512_hash(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-bz2-archive-sha512-hash')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected hash')

class Test_wrong_tar_bz2_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_zip_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_zip_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha1-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_zip_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_zip_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_zip_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_zip_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_uid_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_file_uid_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_file_uid_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_file_uid_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_file_uid_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_file_gid_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_file_gid_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_file_gid_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_file_gid_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_file_gid_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_unexpected_file_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test_unexpected_file_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test_unexpected_file_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test_unexpected_file_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test_unexpected_file_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test_unexpected_file_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test_wrong_file_md5_hash_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha1_hash_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha224_hash_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha256_hash_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha384_hash_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha512_hash_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_md5_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha1_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha224_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha256_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha384_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha512_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_md5_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha1_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha224_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha256_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha384_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha512_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_md5_hash_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha1_hash_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha224_hash_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha256_hash_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha384_hash_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha512_hash_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_md5_hash_in_bzip2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-bzip2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha1_hash_in_bzip2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-bzip2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha224_hash_in_bzip2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-bzip2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha256_hash_in_bzip2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-bzip2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha384_hash_in_bzip2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-bzip2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha512_hash_in_bzip2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-bzip2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_md5_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha1_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha224_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha256_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha384_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')


class Test_wrong_file_sha512_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_md5_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha1_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha224_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha256_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha384_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha512_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_mode_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-mode-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_file_mode_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-mode-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_file_mode_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-mode-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_file_mode_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-mode-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_file_type_f_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-f-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_f_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-f-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_f_in_zip_archive(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-f-in-zip-archive')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected type')


class Test_wrong_file_type_f_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-f-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_d_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-d-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_d_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-d-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_d_in_zip_archive(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-d-in-zip-archive')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected type')

class Test_wrong_file_type_d_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-d-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_corrupted_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('data corruption')

class Test_corrupted_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('data corruption')

class Test_corrupted_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('data corruption')

class Test_corrupted_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('data corruption')

class Test_two_confs_with_the_same_name(Main):
    def __init__(self, q):
        self.__queue = q
        self.__testname = self.__class__.__name__
        self.__testdir = os.path.join(ABSPATH, 'functional-tests/two_confs_with_the_same_name')
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __command = ' '.join([PYTHONEXE, EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        else:
            __command = ' '.join([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        __result = subprocess.getstatusoutput(__command)
        if __result[0] != 0 and 'Please rename it.' in __result[1]:
            self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
        else:
            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(__result[0])))

class Test_expected_file_greater_than_file_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test_expected_file_greater_than_file_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test_expected_file_greater_than_file_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test_expected_file_greater_than_file_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test_expected_file_greater_than_file_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test_expected_file_greater_than_file_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test_expected_file_smaller_than_file_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test_expected_file_smaller_than_file_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test_expected_file_smaller_than_file_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test_expected_file_smaller_than_file_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test_expected_file_smaller_than_file_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test_expected_file_smaller_than_file_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test_expected_file_not_equals_file_in_tar_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-tar-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_expected_file_not_equals_file_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_expected_file_not_equals_file_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_expected_file_not_equals_file_in_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_expected_file_not_equals_file_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_expected_file_not_equals_file_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_mixing_dir_path_and_archive_type_in_conf(Main):
    '''Check if the configuration path indicates a directory while
       the type of the backup is an archive
    '''
    def __init__(self, q):
        self.__queue = q
        self.__testname = self.__class__.__name__
        self.__testdir = os.path.join(ABSPATH, 'functional-tests/mixing-dir-path-and-archive-type-in-conf')
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __command = ' '.join([PYTHONEXE, EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        else:
            __command = ' '.join([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        __result = subprocess.getstatusoutput(__command)
        if __result[0] != 0 and 'is a directory but appears as an archive' in __result[1]:
            self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
        else:
            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(__result[0])))

class Test_full_criteria_multiple_backups:
    '''Check all the itemps for a tar.gz, tar.bz2, gzip, zip and tree'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/full-criteria-multiple-backups')
        __resultfile = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __resultfile])
        else:
            __retcode = subprocess.call([EXE, OPTCONFIG, __testdir, OPTLOG, __resultfile])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                __conditions = {'file missing in': 0,
                'with unexpected mode': 0,
                'with unexpected uid': 0,
                'with unexpected gid': 0,
                'with unexpected hash while checking': 0,
                'bigger than': 0,
                }
                for __line in __file.readlines():
                    for __condition in __conditions:
                        if __condition in __line: 
                            __conditions[__condition] += 1
                for __condition in __conditions:
                    if __conditions[__condition] != 5:
                        __res = False
                if __res:
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_name_in_gzip_and_gzip_archive_are_not_the_same(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/name-in-gzip-and-gzip-archive-are-not-the-same')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('unexpected file checking')
            
class Test_unsupported_parameters_for_gz_archive:
    '''Check for unsupported parameters for a gz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/unsupported-parameters-gz-archive')
        __resultfile = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __resultfile])
        else:
            __retcode = subprocess.call([EXE, OPTCONFIG, __testdir, OPTLOG, __resultfile])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                __conditions = {'Ignoring it': 0,
                }
                for __line in __file.readlines():
                    for __condition in __conditions:
                        if __condition in __line: 
                            __conditions[__condition] += 1
                for __condition in __conditions:
                    if __conditions[__condition] != 3:
                        __res = False
                if __res:
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_unsupported_parameters_for_bz2_archive:
    '''Check for unsupported parameters for a bzip2 archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/unsupported-parameters-bz2-archive')
        __resultfile = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __resultfile])
        else:
            __retcode = subprocess.call([EXE, OPTCONFIG, __testdir, OPTLOG, __resultfile])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                __conditions = {'Ignoring it': 0,
                }
                for __line in __file.readlines():
                    for __condition in __conditions:
                        if __condition in __line: 
                            __conditions[__condition] += 1
                for __condition in __conditions:
                    if __conditions[__condition] != 4:
                        __res = False
                if __res:
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))


class Test_generate_list_for_tar_archive:
    '''Check the expected result for list of files generated from a tar archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-from-tar-archive')
        __archive = os.path.join(__testdir, 'generate-list-from-tar-archive.tar.gz')
        __resultfile = os.path.join(__testdir, 'generate-list-from-tar-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                __conditions = {'=': 0,
                    'uid': 0, 
                    'gid': 0, 
                    'type': 0, 
                    'mode': 0,
                    'md5': 2
                }
                for __line in __file.readlines():
                    for __condition in __conditions:
                        if __condition in __line: 
                            __conditions[__condition] += 1
                for __condition in __conditions:
                    if __conditions[__condition] != 6:
                        __res = False
                if __res:
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_for_zip_archive:
    '''Check the expected result for list of files generated from a zip archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-from-zip-archive')
        __archive = os.path.join(__testdir, 'generate-list-from-zip-archive.zip')
        __resultfile = os.path.join(__testdir, 'generate-list-from-zip-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                __conditions = {'=': 0,
                    'uid': 0, 
                    'gid': 0, 
                    'type': 0, 
                    'mode': 0 
                }
                for __line in __file.readlines():
                    for __condition in __conditions:
                        if __condition in __line: 
                            __conditions[__condition] += 1
                for __condition in __conditions:
                    if __conditions[__condition] != 6:
                        __res = False
                if __res:
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_for_tree:
    '''Check the expected result for list of files generated from a tree of files'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-from-tree')
        __archive = os.path.join(__testdir, 'generate-list-from-tree')
        __resultfile = os.path.join(__testdir, 'generate-list-from-tree.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                __conditions = {'=': 0,
                    'uid': 0, 
                    'gid': 0, 
                    'type': 0, 
                    'mode': 0 
                }
                for __line in __file.readlines():
                    for __condition in __conditions:
                        if __condition in __line: 
                            __conditions[__condition] += 1
                for __condition in __conditions:
                    if __conditions[__condition] != 5:
                        __res = False
                if __res:
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_for_bzip2:
    '''Check the expected result for list of files generated from a bzip2 archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-from-bzip2-archive')
        __archive = os.path.join(__testdir, 'generate-list-from-bzip2-archive.bz2')
        __resultfile = os.path.join(__testdir, 'generate-list-from-bzip2-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                __conditions = {'type': 0, 
                    'md5':0 
                }
                for __line in __file.readlines():
                    for __condition in __conditions:
                        if __condition in __line: 
                            __conditions[__condition] += 1
                for __condition in __conditions:
                    if __conditions[__condition] != 1:
                        __res = False
                if __res:
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_for_xz:
    '''Check the expected result for list of files generated from a xz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-from-xz-archive')
        __archive = os.path.join(__testdir, 'generate-list-from-xz-archive.xz')
        __resultfile = os.path.join(__testdir, 'generate-list-from-xz-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                __conditions = {'type': 0, 
                    'md5':0 
                }
                for __line in __file.readlines():
                    for __condition in __conditions:
                        if __condition in __line: 
                            __conditions[__condition] += 1
                for __condition in __conditions:
                    if __conditions[__condition] != 1:
                        __res = False
                if __res:
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_for_gzip:
    '''Check the expected result for list of files generated from a gzip archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-from-gzip-archive')
        __archive = os.path.join(__testdir, 'generate-list-from-gzip-archive.gz')
        __resultfile = os.path.join(__testdir, 'generate-list-from-gzip-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                __conditions = {'=': 0,
                    'type': 0, 
                    'md5':0 
                }
                for __line in __file.readlines():
                    for __condition in __conditions:
                        if __condition in __line: 
                            __conditions[__condition] += 1
                for __condition in __conditions:
                    if __conditions[__condition] != 1:
                        __res = False
                if __res:
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_expected_generated_list_for_tar_archive:
    '''Compare the generated list and the expected list for a tar archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/expected-generated-list-for-tar-archive')
        __archive = os.path.join(__testdir, 'expected-generated-list-for-tar-archive.tar.gz')
        __resultfile = os.path.join(__testdir, 'expected-generated-list-for-tar-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultfile, 'rb').read()).hexdigest() != hashlib.md5(open(os.path.join(__testdir, 'expectedlist.list'), 'rb').read()).hexdigest():
                __res = False
            else:
                __res = True
            if __res:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_expected_generated_list_for_zip_archive:
    '''Compare the generated list and the expected list for a zip archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/expected-generated-list-for-zip-archive')
        __archive = os.path.join(__testdir, 'expected-generated-list-for-zip-archive.zip')
        __resultfile = os.path.join(__testdir, 'expected-generated-list-for-zip-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultfile, 'rb').read()).hexdigest() != hashlib.md5(open(os.path.join(__testdir, 'expectedlist.list'), 'rb').read()).hexdigest():
                __res = False
            else:
                __res = True
            if __res:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_expected_generated_list_for_gzip_archive:
    '''Compare the generated list and the expected list for a gzip archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/expected-generated-list-for-gzip-archive')
        __archive = os.path.join(__testdir, 'expected-generated-list-for-gzip-archive.gz')
        __resultfile = os.path.join(__testdir, 'expected-generated-list-for-gzip-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultfile, 'rb').read()).hexdigest() != hashlib.md5(open(os.path.join(__testdir, 'expectedlist.list'), 'rb').read()).hexdigest():
                __res = False
            else:
                __res = True
            if __res:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_expected_generated_list_for_bzip2_archive:
    '''Compare the generated list and the expected list for a bzip2 archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/expected-generated-list-for-bzip2-archive')
        __archive = os.path.join(__testdir, 'expected-generated-list-for-bzip2-archive.bz2')
        __resultfile = os.path.join(__testdir, 'expected-generated-list-for-bzip2-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultfile, 'rb').read()).hexdigest() != hashlib.md5(open(os.path.join(__testdir, 'expectedlist.list'), 'rb').read()).hexdigest():
                __res = False
            else:
                __res = True
            if __res:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_and_parse_tar_archive(MainGenerateParse):
    '''Generate a list of files inside the tar archive and parse this one right after'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-and-parse-tar-archive')
        __archive = os.path.join(__testdir, 'generate-list-and-parse-tar-archive.tar.gz')
        __resultfile = os.path.join(__testdir, 'generate-list-and-parse-tar-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            self._queue = q
            self._testname = __testname
            self._testdir = __testdir
            self._resultfile = os.path.join(self._testdir, 'a.out')
            self._main('')

class Test_generate_list_and_parse_zip_archive(MainGenerateParse):
    '''Generate a list of files inside the zip archive and parse this one right after'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-and-parse-zip-archive')
        __archive = os.path.join(__testdir, 'generate-list-and-parse-zip-archive.zip')
        __resultfile = os.path.join(__testdir, 'generate-list-and-parse-zip-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            self._queue = q
            self._testname = __testname
            self._testdir = __testdir
            self._resultfile = os.path.join(self._testdir, 'a.out')
            self._main('')

class Test_generate_list_and_parse_tree(MainGenerateParse):
    '''Generate a list of files inside a tree of files and parse this one right after'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-and-parse-tree')
        __archive = os.path.join(__testdir, 'generate-list-and-parse-tree')
        __resultfile = os.path.join(__testdir, 'generate-list-and-parse-tree.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            self._queue = q
            self._testname = __testname
            self._testdir = __testdir
            self._resultfile = os.path.join(self._testdir, 'a.out')
            self._main('')

class Test_generate_list_and_parse_gzip_archive(MainGenerateParse):
    '''Generate a list of files inside a gzip archive and parse this one right after'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-and-parse-gzip-archive')
        __archive = os.path.join(__testdir, 'generate-list-and-parse-gzip-archive.gz')
        __resultfile = os.path.join(__testdir, 'generate-list-and-parse-gzip-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            self._queue = q
            self._testname = __testname
            self._testdir = __testdir
            self._resultfile = os.path.join(self._testdir, 'a.out')
            self._main('')

class Test_generate_list_and_parse_bzip2_archive(MainGenerateParse):
    '''Generate a list of files inside a bzip2 archive and parse this one right after'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-and-parse-bzip2-archive')
        __archive = os.path.join(__testdir, 'generate-list-and-parse-bzip2-archive.bz2')
        __resultfile = os.path.join(__testdir, 'generate-list-and-parse-bzip2-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            self._queue = q
            self._testname = __testname
            self._testdir = __testdir
            self._resultfile = os.path.join(self._testdir, 'a.out')
            self._main('')

class Test_user_specified_delimiter(Main):
    '''Test if a file is missing in a tar archive with a user-specified delimiter in the file of filenames'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/user-specified-delimiter')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test_tar_archive_size_not_equals_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-archive-size-not-equals-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_tar_gz_archive_size_not_equals_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-gz-archive-size-not-equals-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_tar_bz2_archive_size_not_equals_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-bz2-archive-size-not-equals-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_gzip_archive_size_not_equals_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/gzip-archive-size-not-equals-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_bzip2_archive_size_not_equals_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/bzip2-archive-size-not-equals-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test_zip_archive_size_not_equals_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/zip-archive-size-not-equals-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')

class Test_tar_archive_size_bigger_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-archive-size-bigger-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than')
            
class Test_tar_gz_archive_size_bigger_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-gz-archive-size-bigger-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than')
            
class Test_tar_bz2_archive_size_bigger_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-bz2-archive-size-bigger-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than')
            
class Test_gzip_archive_size_bigger_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/gzip-archive-size-bigger-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than')
            
class Test_bzip2_archive_size_bigger_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/bzip2-archive-size-bigger-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than')
            
class Test_zip_archive_size_bigger_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/zip-archive-size-bigger-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than')

class Test_tar_archive_size_smaller_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-archive-size-smaller-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than')
            
class Test_tar_gz_archive_size_smaller_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-gz-archive-size-smaller-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than')
            
class Test_tar_bz2_archive_size_smaller_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-bz2-archive-size-smaller-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than')
            
class Test_zip_archive_size_smaller_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/zip-archive-size-smaller-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than')
            
class Test_gzip_archive_size_smaller_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/gzip-archive-size-smaller-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than')
            
class Test_bzip2_archive_size_smaller_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/bzip2-archive-size-smaller-than-expected-size')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than')
            
if __name__ == '__main__':
    processes = []
    results = []
    koresults = []
    q = Queue()

    for element in dir(functionaltests):
        if 'Test' in element:
            processes.append(Process(target=getattr(functionaltests, element), args=(q,)))
            processes[-1].start()
    for p in processes:
        results.append(q.get())
        p.join()
    # Establishing list of KOs
    for result in results:
        if KOMSG in result:
            koresults.append(result)
    if len(koresults) != 0:
        print(linesep.join(koresults))
        sys.exit(1)
    else:
        print(linesep.join(results))
