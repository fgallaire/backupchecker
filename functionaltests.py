#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# Copyright © 2015 Carl Chenet <chaica@backupcheckerproject.org>
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
from os import linesep, environ, link, remove
import subprocess
import os.path
import shutil
import sys

import functionaltests

EXE = './backupchecker.py'
OPTCONFIG = '-c'
OPTOUTPUTCONFDIR = '-C'
OPTOUTPUTLISTDIR = '-L'
OPTCONFNAME = '-n'
OPTDEL = '-d'
OPTEXCEPTIONSFILE = '-E'
OPTGEN = '-g'
OPTFULLGEN = '-G'
OPTHASHTYPE = '--hashtype'
OPTHASHES = '-H'
OPTLOG = '-l'
OKMSG = 'ok'
KOMSG = 'ko - '
PYTHONEXE =''
ABSPATH = ''
ALTERNATEDELIMITER = '('

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

class Test_file_missing_in_xz(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-xz')
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

class Test_wrong_tar_xz_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-xz-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_gzip_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test_wrong_xz_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-xz-archive-mode')
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

class Test_wrong_tar_xz_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-xz-archive-uid')
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

class Test_wrong_bzip2_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-bz2-archive-uid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test_wrong_xz_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-xz-archive-uid')
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

class Test_wrong_tar_xz_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-xz-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_gzip_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_bzip2_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-bz2-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test_wrong_xz_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-xz-archive-gid')
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

class Test_wrong_tar_xz_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-xz-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_gz_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_xz_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-xz-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_gz_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_xz_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-xz-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_gz_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_xz_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-xz-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_bz2_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_xz_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-xz-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_bz2_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha1-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_tar_xz_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-xz-archive-sha1-hash')
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

class Test_wrong_xz_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-xz-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_xz_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-xz-archive-md5-hash')
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

class Test_wrong_xz_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-xz-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_gzip_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_xz_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-xz-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_gzip_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_xz_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-xz-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_gzip_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-gz-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_xz_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-xz-archive-sha512-hash')
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

class Test_wrong_file_uid_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-tar-xz-archive')
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

class Test_wrong_file_gid_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-tar-xz-archive')
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

class Test_unexpected_file_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-tar-xz-archive')
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

class Test_wrong_file_md5_hash_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-tar-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha1_hash_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-tar-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha224_hash_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-tar-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha256_hash_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-tar-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha384_hash_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-tar-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha512_hash_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-tar-xz-archive')
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

class Test_wrong_file_md5_hash_in_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha1_hash_in_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha224_hash_in_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha256_hash_in_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha384_hash_in_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test_wrong_file_sha512_hash_in_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-xz-archive')
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

class Test_wrong_file_mode_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-mode-in-tar-xz-archive')
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

class Test_wrong_file_type_f_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-f-in-tar-xz-archive')
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

class Test_wrong_file_type_d_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-d-in-tar-xz-archive')
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

class Test_wrong_file_type_s_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-s-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_s_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-s-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_s_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-s-in-tar-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')


class Test_wrong_file_type_s_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-s-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_l_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-l-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_l_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-l-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test_wrong_file_type_l_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-l-in-tar-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')


class Test_wrong_file_type_l_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-l-in-tree')
        __testsubdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-l-in-tree/wrong-file-type-l-in-tree')
        __mockfile = os.path.join(__testsubdir, 'foo')
        __mocklink = os.path.join(__testsubdir, 'bar')
        if os.path.exists(__testsubdir):
            shutil.rmtree(__testsubdir)
            os.mkdir(__testsubdir)
        else:
            os.mkdir(__testsubdir)
        open(__mockfile, 'w')
        link(__mockfile, __mocklink)
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

class Test_corrupted_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-tar-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('data corruption')

class Test_corrupted_gzip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('data corruption')

class Test_corrupted_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-xz-archive')
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
            
class Test_expected_file_greater_than_file_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-tar-xz-archive')
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
            
class Test_expected_file_smaller_than_file_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-tar-xz-archive')
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
            
class Test_expected_file_not_equals_file_in_tar_xz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-tar-xz-archive')
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

class Test_unsupported_parameters_for_xz_archive:
    '''Check for unsupported parameters for a xz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/unsupported-parameters-xz-archive')
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

class Test_unsupported_parameters_for_zip_archive:
    '''Check for unsupported parameters for a zip archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/unsupported-parameters-zip-archive')
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
                    if __conditions[__condition] != 1:
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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

class Test_expected_generated_list_for_xz_archive:
    '''Compare the generated list and the expected list for a xz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/expected-generated-list-for-xz-archive')
        __archive = os.path.join(__testdir, 'expected-generated-list-for-xz-archive.xz')
        __resultfile = os.path.join(__testdir, 'expected-generated-list-for-xz-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            self._queue = q
            self._testname = __testname
            self._testdir = __testdir
            self._resultfile = os.path.join(self._testdir, 'a.out')
            self._main('')

class Test_generate_list_and_parse_tgz_archive(MainGenerateParse):
    '''Generate a list of files inside the tgz (same as tar.gz) archive and parse this one right after'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-and-parse-tgz-archive')
        __archive = os.path.join(__testdir, 'generate-list-and-parse-tgz-archive.tgz')
        __resultfile = os.path.join(__testdir, 'generate-list-and-parse-tgz-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            self._queue = q
            self._testname = __testname
            self._testdir = __testdir
            self._resultfile = os.path.join(self._testdir, 'a.out')
            self._main('')

class Test_generate_list_and_parse_tbz_archive(MainGenerateParse):
    '''Generate a list of files inside the tbz (same as tar.bz2) archive and parse this one right after'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-and-parse-tbz-archive')
        __archive = os.path.join(__testdir, 'generate-list-and-parse-tbz-archive.tbz')
        __resultfile = os.path.join(__testdir, 'generate-list-and-parse-tbz-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            self._queue = q
            self._testname = __testname
            self._testdir = __testdir
            self._resultfile = os.path.join(self._testdir, 'a.out')
            self._main('')

class Test_generate_list_and_parse_tbz2_archive(MainGenerateParse):
    '''Generate a list of files inside the tbz2 (same as tar.bz2) archive and parse this one right after'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-and-parse-tbz2-archive')
        __archive = os.path.join(__testdir, 'generate-list-and-parse-tbz2-archive.tbz2')
        __resultfile = os.path.join(__testdir, 'generate-list-and-parse-tbz2-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            self._queue = q
            self._testname = __testname
            self._testdir = __testdir
            self._resultfile = os.path.join(self._testdir, 'a.out')
            self._main('')

class Test_generate_list_and_parse_xz_archive(MainGenerateParse):
    '''Generate a list of files inside a xz archive and parse this one right after'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-and-parse-xz-archive')
        __archive = os.path.join(__testdir, 'generate-list-and-parse-xz-archive.xz')
        __resultfile = os.path.join(__testdir, 'generate-list-and-parse-xz-archive.list')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
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

class Test_tar_xz_archive_size_not_equals_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-xz-archive-size-not-equals-expected-size')
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
            
class Test_tar_xz_archive_size_bigger_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-xz-archive-size-bigger-than-expected-size')
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
            
class Test_tar_xz_archive_size_smaller_than_expected_size(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/tar-xz-archive-size-smaller-than-expected-size')
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

class Test_checkarchive_supported_types_equals_listtype_supported_types:
    '''Test if the supported types in checkarchives.py equals the ones in
       listtype.py
       This is not exactly a functional test but it triggered bug #24 so
       it needs to be tested  
    '''
    def __init__(self, q):
        # extract supported extensions from the code
        # store them in sets and compare them
        __queue = q
        __testname = self.__class__.__name__
        with open('backupchecker/checkbackups/checkbackups.py') as __f1:
            __checkarchivescode = __f1.readlines()
        with open('backupchecker/listtype.py') as __f2:
            __listtypecode = __f2.readlines()
        __checkarchivestypes = set()
        __listtypetypes = set()
        for __line in __checkarchivescode:
            if 'endswith' in __line:
                __checkarchivestypes.add(__line.split(".endswith('")[1].split("'")[0])
        for __line in __listtypecode:
            if 'endswith' in __line:
                __listtypetypes.add(__line.split(".endswith('")[1].split("'")[0])
        # symmetrical differences of the two sets
        __unsupportedtypes = __checkarchivestypes ^ __listtypetypes
        if not __unsupportedtypes:
            __queue.put('{} - {}'.format(__testname, OKMSG))
        else:
            __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            
class Test_generate_list_changing_default_separator_for_tar_gz:
    '''Generate a list of files changing the default separator for tar gz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-changing-default-separator/tar.gz')
        __archive = os.path.join(__testdir, 'generate-list-changing-default-separator-for-tar-gz.tar.gz')
        __resultfile = os.path.join(__testdir, 'generate-list-changing-default-separator-for-tar-gz.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__output, 'r') as __file:
                    if '' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            
class Test_generate_list_changing_default_separator_for_tar_bz2:
    '''Generate a list of files changing the default separator for tar bz2 archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-changing-default-separator/tar.bz2')
        __archive = os.path.join(__testdir, 'generate-list-changing-default-separator-for-tar-bz2.tar.bz2')
        __resultfile = os.path.join(__testdir, 'generate-list-changing-default-separator-for-tar-bz2.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__output, 'r') as __file:
                    if '' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            
class Test_generate_list_changing_default_separator_for_tar_xz:
    '''Generate a list of files changing the default separator for tar xz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-changing-default-separator/tar.xz')
        __archive = os.path.join(__testdir, 'generate-list-changing-default-separator-for-tar-xz.tar.xz')
        __resultfile = os.path.join(__testdir, 'generate-list-changing-default-separator-for-tar-xz.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__output, 'r') as __file:
                    if '' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
        
class Test_generate_list_changing_default_separator_for_gzip:
    '''Generate a list of files changing the default separator for gzip archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-changing-default-separator/gzip')
        __archive = os.path.join(__testdir, 'generate-list-changing-default-separator-for-gzip.gz')
        __resultfile = os.path.join(__testdir, 'generate-list-changing-default-separator-for-gzip.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__output, 'r') as __file:
                    if '' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            
class Test_generate_list_changing_default_separator_for_bzip2:
    '''Generate a list of files changing the default separator for bzip2 archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-changing-default-separator/bzip2')
        __archive = os.path.join(__testdir, 'generate-list-changing-default-separator-for-bzip2.bz2')
        __resultfile = os.path.join(__testdir, 'generate-list-changing-default-separator-for-bzip2.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__output, 'r') as __file:
                    if '' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_changing_default_separator_for_zip:
    '''Generate a list of files changing the default separator for zip archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-changing-default-separator/zip')
        __archive = os.path.join(__testdir, 'generate-list-changing-default-separator-for-zip.zip')
        __resultfile = os.path.join(__testdir, 'generate-list-changing-default-separator-for-zip.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__output, 'r') as __file:
                    if '' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_changing_default_separator_for_tree:
    '''Generate a list of files changing the default separator for a tree of files'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-list-changing-default-separator/tree')
        __archive = os.path.join(__testdir, 'generate-list-changing-default-separator-for-tree')
        __resultfile = os.path.join(__testdir, 'generate-list-changing-default-separator-for-tree.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTDEL, ALTERNATEDELIMITER, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__output, 'r') as __file:
                    if '' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_expecting_hard_link_for_tar_gz(Main):
    '''Test if an expecting hard link in a tar.gz archive fails on a regular file'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expecting-hard-link-for-tar-gz')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('is a regular file. Should have been a hard link')

class Test_wrong_target_in_tar_gz_archive(Main):
    '''Test if the target of a symlink is wrong in a tar gz archive'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-target-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main(' target is')

class Test_wrong_target_in_tar_bz2_archive(Main):
    '''Test if the target of a symlink is wrong in a tar bz2 archive'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-target-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main(' target is')

class Test_wrong_target_in_tar_xz_archive(Main):
    '''Test if the target of a symlink is wrong in a tar xz archive'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-target-in-tar-xz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main(' target is')

class Test_wrong_target_in_tree(Main):
    '''Test if the target of a symlink is wrong in a tree of files'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-target-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main(' target is')


class Test_generate_conf_and_file_list_tar:
    '''Compare the generated list and the expected list and the configuration file and the expected configuration file for a tar archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-conf-and-file-list-tar')
        __archive = os.path.join(__testdir, 'generate-conf-and-file-list-tar.tar')
        __conffile = os.path.join(__testdir, 'conf.conf')
        __listfile = os.path.join(__testdir, 'list.list')
        __origconffile = os.path.join(__testdir, 'conf.conf.bck')
        __resultconffile = os.path.join(__testdir, 'generate-conf-and-file-list-tar.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-conf-and-file-list-tar.list')
        __newconffile = []
        # prepare the environment
        shutil.copyfile(__origconffile, __conffile)
        # switch flags expected conf and list files to good environment variables
        with open(__conffile) as __objconf:
            for __line in __objconf.readlines():
                if 'PATH' in __line:
                    __line = __line.replace('PATH', os.path.abspath('functional-tests/generate-conf-and-file-list-tar'))
                __newconffile.append(__line)
        with open(__conffile, 'w') as __objconf:
            __objconf.writelines(__newconffile)
 
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultconffile, 'rb').read()).hexdigest() != hashlib.md5(open(__conffile, 'rb').read()).hexdigest():
                __confres = False
            else:
                __confres = True
            if hashlib.md5(open(__resultlistfile, 'rb').read()).hexdigest() != hashlib.md5(open(__listfile, 'rb').read()).hexdigest():
                __listres = False
            else:
                __listres = True
            if __confres and __listres:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_conf_and_file_list_tar_gz:
    '''Compare the generated list and the expected list and the configuration file and the expected configuration file for a tar gz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-conf-and-file-list-tar-gz')
        __archive = os.path.join(__testdir, 'generate-conf-and-file-list-tar-gz.tar.gz')
        __conffile = os.path.join(__testdir, 'conf.conf')
        __listfile = os.path.join(__testdir, 'list.list')
        __origconffile = os.path.join(__testdir, 'conf.conf.bck')
        __resultconffile = os.path.join(__testdir, 'generate-conf-and-file-list-tar-gz.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-conf-and-file-list-tar-gz.list')
        __newconffile = []
        # prepare the environment
        shutil.copyfile(__origconffile, __conffile)
        # switch flags expected conf and list files to good environment variables
        with open(__conffile) as __objconf:
            for __line in __objconf.readlines():
                if 'PATH' in __line:
                    __line = __line.replace('PATH', os.path.abspath('functional-tests/generate-conf-and-file-list-tar-gz'))
                __newconffile.append(__line)
        with open(__conffile, 'w') as __objconf:
            __objconf.writelines(__newconffile)
 
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultconffile, 'rb').read()).hexdigest() != hashlib.md5(open(__conffile, 'rb').read()).hexdigest():
                __confres = False
            else:
                __confres = True
            if hashlib.md5(open(__resultlistfile, 'rb').read()).hexdigest() != hashlib.md5(open(__listfile, 'rb').read()).hexdigest():
                __listres = False
            else:
                __listres = True
            if __confres and __listres:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_conf_and_file_list_tar_bz2:
    '''Compare the generated list and the expected list and the configuration file and the expected configuration file for a tar bz2 archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-conf-and-file-list-tar-bz2')
        __archive = os.path.join(__testdir, 'generate-conf-and-file-list-tar-bz2.tar.bz2')
        __conffile = os.path.join(__testdir, 'conf.conf')
        __listfile = os.path.join(__testdir, 'list.list')
        __origconffile = os.path.join(__testdir, 'conf.conf.bck')
        __resultconffile = os.path.join(__testdir, 'generate-conf-and-file-list-tar-bz2.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-conf-and-file-list-tar-bz2.list')
        __newconffile = []
        # prepare the environment
        shutil.copyfile(__origconffile, __conffile)
        # switch flags expected conf and list files to good environment variables
        with open(__conffile) as __objconf:
            for __line in __objconf.readlines():
                if 'PATH' in __line:
                    __line = __line.replace('PATH', os.path.abspath('functional-tests/generate-conf-and-file-list-tar-bz2'))
                __newconffile.append(__line)
        with open(__conffile, 'w') as __objconf:
            __objconf.writelines(__newconffile)
 
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultconffile, 'rb').read()).hexdigest() != hashlib.md5(open(__conffile, 'rb').read()).hexdigest():
                __confres = False
            else:
                __confres = True
            if hashlib.md5(open(__resultlistfile, 'rb').read()).hexdigest() != hashlib.md5(open(__listfile, 'rb').read()).hexdigest():
                __listres = False
            else:
                __listres = True
            if __confres and __listres:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_conf_and_file_list_tar_xz:
    '''Compare the generated list and the expected list and the configuration file and the expected configuration file for a tar xz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-conf-and-file-list-tar-xz')
        __archive = os.path.join(__testdir, 'generate-conf-and-file-list-tar-xz.tar.xz')
        __conffile = os.path.join(__testdir, 'conf.conf')
        __listfile = os.path.join(__testdir, 'list.list')
        __origconffile = os.path.join(__testdir, 'conf.conf.bck')
        __resultconffile = os.path.join(__testdir, 'generate-conf-and-file-list-tar-xz.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-conf-and-file-list-tar-xz.list')
        __newconffile = []
        # prepare the environment
        shutil.copyfile(__origconffile, __conffile)
        # switch flags expected conf and list files to good environment variables
        with open(__conffile) as __objconf:
            for __line in __objconf.readlines():
                if 'PATH' in __line:
                    __line = __line.replace('PATH', os.path.abspath('functional-tests/generate-conf-and-file-list-tar-xz'))
                __newconffile.append(__line)
        with open(__conffile, 'w') as __objconf:
            __objconf.writelines(__newconffile)
 
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultconffile, 'rb').read()).hexdigest() != hashlib.md5(open(__conffile, 'rb').read()).hexdigest():
                __confres = False
            else:
                __confres = True
            if hashlib.md5(open(__resultlistfile, 'rb').read()).hexdigest() != hashlib.md5(open(__listfile, 'rb').read()).hexdigest():
                __listres = False
            else:
                __listres = True
            if __confres and __listres:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_conf_and_file_list_gz:
    '''Compare the generated list and the expected list and the configuration file and the expected configuration file for a gz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-conf-and-file-list-gz')
        __archive = os.path.join(__testdir, 'generate-conf-and-file-list-gz.gz')
        __conffile = os.path.join(__testdir, 'conf.conf')
        __listfile = os.path.join(__testdir, 'list.list')
        __origconffile = os.path.join(__testdir, 'conf.conf.bck')
        __resultconffile = os.path.join(__testdir, 'generate-conf-and-file-list-gz.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-conf-and-file-list-gz.list')
        __newconffile = []
        # prepare the environment
        shutil.copyfile(__origconffile, __conffile)
        # switch flags expected conf and list files to good environment variables
        with open(__conffile) as __objconf:
            for __line in __objconf.readlines():
                if 'PATH' in __line:
                    __line = __line.replace('PATH', os.path.abspath('functional-tests/generate-conf-and-file-list-gz'))
                __newconffile.append(__line)
        with open(__conffile, 'w') as __objconf:
            __objconf.writelines(__newconffile)
 
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultconffile, 'rb').read()).hexdigest() != hashlib.md5(open(__conffile, 'rb').read()).hexdigest():
                __confres = False
            else:
                __confres = True
            if hashlib.md5(open(__resultlistfile, 'rb').read()).hexdigest() != hashlib.md5(open(__listfile, 'rb').read()).hexdigest():
                __listres = False
            else:
                __listres = True
            if __confres and __listres:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_conf_and_file_list_bz2:
    '''Compare the generated list and the expected list and the configuration file and the expected configuration file for a bz2 archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-conf-and-file-list-bz2')
        __archive = os.path.join(__testdir, 'generate-conf-and-file-list-bz2.bz2')
        __conffile = os.path.join(__testdir, 'conf.conf')
        __listfile = os.path.join(__testdir, 'list.list')
        __origconffile = os.path.join(__testdir, 'conf.conf.bck')
        __resultconffile = os.path.join(__testdir, 'generate-conf-and-file-list-bz2.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-conf-and-file-list-bz2.list')
        __newconffile = []
        # prepare the environment
        shutil.copyfile(__origconffile, __conffile)
        # switch flags expected conf and list files to good environment variables
        with open(__conffile) as __objconf:
            for __line in __objconf.readlines():
                if 'PATH' in __line:
                    __line = __line.replace('PATH', os.path.abspath('functional-tests/generate-conf-and-file-list-bz2'))
                __newconffile.append(__line)
        with open(__conffile, 'w') as __objconf:
            __objconf.writelines(__newconffile)
 
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultconffile, 'rb').read()).hexdigest() != hashlib.md5(open(__conffile, 'rb').read()).hexdigest():
                __confres = False
            else:
                __confres = True
            if hashlib.md5(open(__resultlistfile, 'rb').read()).hexdigest() != hashlib.md5(open(__listfile, 'rb').read()).hexdigest():
                __listres = False
            else:
                __listres = True
            if __confres and __listres:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_conf_and_file_list_xz:
    '''Compare the generated list and the expected list and the configuration file and the expected configuration file for a xz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-conf-and-file-list-xz')
        __archive = os.path.join(__testdir, 'generate-conf-and-file-list-xz.xz')
        __conffile = os.path.join(__testdir, 'conf.conf')
        __listfile = os.path.join(__testdir, 'list.list')
        __origconffile = os.path.join(__testdir, 'conf.conf.bck')
        __resultconffile = os.path.join(__testdir, 'generate-conf-and-file-list-xz.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-conf-and-file-list-xz.list')
        __newconffile = []
        # prepare the environment
        shutil.copyfile(__origconffile, __conffile)
        # switch flags expected conf and list files to good environment variables
        with open(__conffile) as __objconf:
            for __line in __objconf.readlines():
                if 'PATH' in __line:
                    __line = __line.replace('PATH', os.path.abspath('functional-tests/generate-conf-and-file-list-xz'))
                __newconffile.append(__line)
        with open(__conffile, 'w') as __objconf:
            __objconf.writelines(__newconffile)
 
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if hashlib.md5(open(__resultconffile, 'rb').read()).hexdigest() != hashlib.md5(open(__conffile, 'rb').read()).hexdigest():
                __confres = False
            else:
                __confres = True
            if hashlib.md5(open(__resultlistfile, 'rb').read()).hexdigest() != hashlib.md5(open(__listfile, 'rb').read()).hexdigest():
                __listres = False
            else:
                __listres = True
            if __confres and __listres:
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_conf_and_file_list_tree:
    '''Compare the generated list and the expected list and the configuration file and the expected configuration file for a tree'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-conf-and-file-list-tree')
        __archive = os.path.join(__testdir, 'generate-conf-and-file-list-tree')
        __resultconffile = os.path.join(__testdir, 'generate-conf-and-file-list-tree.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-conf-and-file-list-tree.list')
        __newconffile = []
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check if the parameter sha512 is available in the configuration file
            if 'sha512' in open(__resultconffile).read():
                __queue.put('{} - {}'.format(__testname, OKMSG))
            else:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_sha_sum_in_conf(Main):
    '''Test if the parameter hash in the configuration file is recognized'''
    def __init__(self, q):
        self.__queue = q
        self.__testname = self.__class__.__name__
        self.__testdir = os.path.join(ABSPATH, 'functional-tests/sha-sum-in-conf')
        self.__resultfile = os.path.join(self.__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __command = ' '.join([PYTHONEXE, EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        else:
            __command = ' '.join([EXE, OPTCONFIG, self.__testdir, OPTLOG, self.__resultfile])
        __result = subprocess.getstatusoutput(__command)
        if __result[0] != 0:
            self.__queue.put('{} - {}'.format(self.__testname, OKMSG))
        else:
            self.__queue.put('{} - {}return code:{}'.format(self.__testname, KOMSG, str(__result[0])))

class Test_missing_gpg_footer(Main):
    '''Test if the pgp/gpg footer is missing in the configuration file'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/missing-gpg-footer')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.getstatusoutput(' '.join([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output]))
        else:
            __retcode = subprocess.getstatusoutput(' '.join([EXE, OPTCONFIG, __testdir, OPTLOG, __output]))
        if __retcode[0] != 0:
            __queue.put('{} - {}'.format(__testname, OKMSG))
        else:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode[0])))

class Test_missing_gpg_header(Main):
    '''Test if the gpg/pgp header is missing in the configuration file'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/missing-gpg-header')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.getstatusoutput(' '.join([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output]))
        else:
            __retcode = subprocess.getstatusoutput(' '.join([EXE, OPTCONFIG, __testdir, OPTLOG, __output]))
        if __retcode[0] != 0:
            __queue.put('{} - {}'.format(__testname, OKMSG))
        else:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode[0])))

class Test_strip_gpg_header_tar_gz(Main):
    '''Test if the gpg/pgp header is removed effectively on tar gz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/strip-gpg-header-tar-gz')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.getstatusoutput(' '.join([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output]))
        else:
            __retcode = subprocess.getstatusoutput(' '.join([EXE, OPTCONFIG, __testdir, OPTLOG, __output]))
        if __retcode[0] == 0:
            __queue.put('{} - {}'.format(__testname, OKMSG))
        else:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode[1])))

class Test_generate_list_to_check_mtime_in_tar_archive:
    '''Generate a list of files to check that mtime in tar archive is written'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/check-mtime-tar')
        __archive = os.path.join(__testdir, 'check-mtime-tar.tar.gz')
        __resultfile = os.path.join(__testdir, 'check-mtime-tar.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__resultfile, 'r') as __file:
                    if ' mtime|' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_to_check_mtime_in_zip_archive:
    '''Generate a list of files to check that mtime in zip archive is written'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/check-mtime-zip')
        __archive = os.path.join(__testdir, 'check-mtime-zip.zip')
        __resultfile = os.path.join(__testdir, 'check-mtime-zip.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__resultfile, 'r') as __file:
                    if ' mtime|' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_to_check_mtime_in_tree:
    '''Generate a list of files to check that mtime in tree is written'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/check-mtime-tree')
        __archive = os.path.join(__testdir, 'check-mtime-tree')
        __resultfile = os.path.join(__testdir, 'check-mtime-tree.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultfile, 'r') as __file:
                if ' mtime|' in __file.read():
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_apk_conf_files:
    '''Generate a apk archive and verify the result'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-apk-conf-files')
        __archive = os.path.join(__testdir, 'generate-apk-conf-files.apk')
        __resultconffile = os.path.join(__testdir, 'generate-apk-conf-files.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-apk-conf-files.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultconffile, 'r') as __file:
                if 'name=generate-apk-conf-files' in __file.read():
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            with open(__resultlistfile, 'r') as __file:
                if 'res/drawable-hdpi/balloons2.png| =7511 uid|0 gid|0 mtime|1329733756.0' in __file.read():
                    __queue.put('{} - {}'.format(__testname, OKMSG))
                else:
                    __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
 
class Test_custom_conf_filelist_tar:
    '''Test to define a custom location to write conf and listfile files for tar archives'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/custom-conf-filelist-tar')
        __confdir = os.path.join(__testdir, 'conf')
        __listdir = os.path.join(__testdir, 'list')
        __bothdir = os.path.join(__testdir, 'both')
        __archive = os.path.join(__testdir, 'custom-conf-filelist-tar.tar.gz')
        __resultconffile = os.path.join(__testdir, 'conf', 'custom-conf-filelist-tar.conf')
        __resultlistfile = os.path.join(__testdir, 'list', 'custom-conf-filelist-tar.list')
        __resultbothconffile = os.path.join(__testdir, 'both', 'custom-conf-filelist-tar.conf')
        __resultbothlistfile = os.path.join(__testdir, 'both', 'custom-conf-filelist-tar.list')
        if not os.path.exists(__confdir):
            os.mkdir(__confdir)
        if not os.path.exists(__listdir):
            os.mkdir(__listdir)
        if not os.path.exists(__bothdir):
            os.mkdir(__bothdir)
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-tar.conf')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-tar.conf'))
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-tar.list')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-tar.list'))
        if os.path.exists(__resultconffile):
            remove(__resultconffile)
        if os.path.exists(__resultlistfile):
            remove(__resultlistfile)
        if os.path.exists(__resultbothconffile):
            remove(__resultbothconffile)
        if os.path.exists(__resultbothlistfile):
            remove(__resultbothlistfile)
        if 'PYTHONEXE' in environ:
            __retcode1 = subprocess.call([PYTHONEXE, EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode1 = subprocess.call([EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode2 = subprocess.call([PYTHONEXE, EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode2 = subprocess.call([EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode3 = subprocess.call([PYTHONEXE, EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode3 = subprocess.call([EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        if __retcode1 != 0 and __retcode2 != 0 and __retcode3 != 0:
            __queue.put('{} - {}return code:{} {} {}'.format(__testname, KOMSG, str(__retcode1), str(__retcode2), str(__retcode3)))
        else:
            if not os.path.exists(__resultconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultconffile))
            elif not os.path.exists(__resultlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultlistfile))
            elif not os.path.exists(__resultbothconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothconffile))
            elif not os.path.exists(__resultbothlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothlistfile))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))
 
class Test_custom_conf_filelist_gzip:
    '''Test to define a custom location to write conf and listfile files for gzip archives'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/custom-conf-filelist-gzip')
        __confdir = os.path.join(__testdir, 'conf')
        __listdir = os.path.join(__testdir, 'list')
        __bothdir = os.path.join(__testdir, 'both')
        __archive = os.path.join(__testdir, 'custom-conf-filelist-gzip.gz')
        __resultconffile = os.path.join(__testdir, 'conf', 'custom-conf-filelist-gzip.conf')
        __resultlistfile = os.path.join(__testdir, 'list', 'custom-conf-filelist-gzip.list')
        __resultbothconffile = os.path.join(__testdir, 'both', 'custom-conf-filelist-gzip.conf')
        __resultbothlistfile = os.path.join(__testdir, 'both', 'custom-conf-filelist-gzip.list')
        if not os.path.exists(__confdir):
            os.mkdir(__confdir)
        if not os.path.exists(__listdir):
            os.mkdir(__listdir)
        if not os.path.exists(__bothdir):
            os.mkdir(__bothdir)
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-gzip.conf')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-gzip.conf'))
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-gzip.list')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-gzip.list'))
        if os.path.exists(__resultconffile):
            remove(__resultconffile)
        if os.path.exists(__resultlistfile):
            remove(__resultlistfile)
        if os.path.exists(__resultbothconffile):
            remove(__resultbothconffile)
        if os.path.exists(__resultbothlistfile):
            remove(__resultbothlistfile)
        if 'PYTHONEXE' in environ:
            __retcode1 = subprocess.call([PYTHONEXE, EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode1 = subprocess.call([EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode2 = subprocess.call([PYTHONEXE, EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode2 = subprocess.call([EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode3 = subprocess.call([PYTHONEXE, EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode3 = subprocess.call([EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        if __retcode1 != 0 and __retcode2 != 0 and __retcode3 != 0:
            __queue.put('{} - {}return code:{} {} {}'.format(__testname, KOMSG, str(__retcode1), str(__retcode2), str(__retcode3)))
        else:
            if not os.path.exists(__resultconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultconffile))
            elif not os.path.exists(__resultlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultlistfile))
            elif not os.path.exists(__resultbothconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothconffile))
            elif not os.path.exists(__resultbothlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothlistfile))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))
 
class Test_custom_conf_filelist_bzip2:
    '''Test to define a custom location to write conf and listfile files for bzip2 archives'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/custom-conf-filelist-bzip2')
        __confdir = os.path.join(__testdir, 'conf')
        __listdir = os.path.join(__testdir, 'list')
        __bothdir = os.path.join(__testdir, 'both')
        __archive = os.path.join(__testdir, 'custom-conf-filelist-bzip2.bz2')
        __resultconffile = os.path.join(__testdir, 'conf', 'custom-conf-filelist-bzip2.conf')
        __resultlistfile = os.path.join(__testdir, 'list', 'custom-conf-filelist-bzip2.list')
        __resultbothconffile = os.path.join(__testdir, 'both', 'custom-conf-filelist-bzip2.conf')
        __resultbothlistfile = os.path.join(__testdir, 'both', 'custom-conf-filelist-bzip2.list')
        if not os.path.exists(__confdir):
            os.mkdir(__confdir)
        if not os.path.exists(__listdir):
            os.mkdir(__listdir)
        if not os.path.exists(__bothdir):
            os.mkdir(__bothdir)
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-bzip2.conf')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-bzip2.conf'))
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-bzip2.list')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-bzip2.list'))
        if os.path.exists(__resultconffile):
            remove(__resultconffile)
        if os.path.exists(__resultlistfile):
            remove(__resultlistfile)
        if os.path.exists(__resultbothconffile):
            remove(__resultbothconffile)
        if os.path.exists(__resultbothlistfile):
            remove(__resultbothlistfile)
        if 'PYTHONEXE' in environ:
            __retcode1 = subprocess.call([PYTHONEXE, EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode1 = subprocess.call([EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode2 = subprocess.call([PYTHONEXE, EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode2 = subprocess.call([EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode3 = subprocess.call([PYTHONEXE, EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode3 = subprocess.call([EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        if __retcode1 != 0 and __retcode2 != 0 and __retcode3 != 0:
            __queue.put('{} - {}return code:{} {} {}'.format(__testname, KOMSG, str(__retcode1), str(__retcode2), str(__retcode3)))
        else:
            if not os.path.exists(__resultconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultconffile))
            elif not os.path.exists(__resultlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultlistfile))
            elif not os.path.exists(__resultbothconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothconffile))
            elif not os.path.exists(__resultbothlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothlistfile))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))
 
class Test_custom_conf_filelist_lzma:
    '''Test to define a custom location to write conf and listfile files for lzma archives'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/custom-conf-filelist-lzma')
        __confdir = os.path.join(__testdir, 'conf')
        __listdir = os.path.join(__testdir, 'list')
        __bothdir = os.path.join(__testdir, 'both')
        __archive = os.path.join(__testdir, 'custom-conf-filelist-lzma.xz')
        __resultconffile = os.path.join(__testdir, 'conf', 'custom-conf-filelist-lzma.conf')
        __resultlistfile = os.path.join(__testdir, 'list', 'custom-conf-filelist-lzma.list')
        __resultbothconffile = os.path.join(__testdir, 'both', 'custom-conf-filelist-lzma.conf')
        __resultbothlistfile = os.path.join(__testdir, 'both', 'custom-conf-filelist-lzma.list')
        if not os.path.exists(__confdir):
            os.mkdir(__confdir)
        if not os.path.exists(__listdir):
            os.mkdir(__listdir)
        if not os.path.exists(__bothdir):
            os.mkdir(__bothdir)
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-lzma.conf')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-lzma.conf'))
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-lzma.list')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-lzma.list'))
        if os.path.exists(__resultconffile):
            remove(__resultconffile)
        if os.path.exists(__resultlistfile):
            remove(__resultlistfile)
        if os.path.exists(__resultbothconffile):
            remove(__resultbothconffile)
        if os.path.exists(__resultbothlistfile):
            remove(__resultbothlistfile)
        if 'PYTHONEXE' in environ:
            __retcode1 = subprocess.call([PYTHONEXE, EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode1 = subprocess.call([EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode2 = subprocess.call([PYTHONEXE, EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode2 = subprocess.call([EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode3 = subprocess.call([PYTHONEXE, EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode3 = subprocess.call([EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        if __retcode1 != 0 and __retcode2 != 0 and __retcode3 != 0:
            __queue.put('{} - {}return code:{} {} {}'.format(__testname, KOMSG, str(__retcode1), str(__retcode2), str(__retcode3)))
        else:
            if not os.path.exists(__resultconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultconffile))
            elif not os.path.exists(__resultlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultlistfile))
            elif not os.path.exists(__resultbothconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothconffile))
            elif not os.path.exists(__resultbothlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothlistfile))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_custom_conf_filelist_zip:
    '''Test to define a custom location to write conf and listfile files for zip archives'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/custom-conf-filelist-zip')
        __confdir = os.path.join(__testdir, 'conf')
        __listdir = os.path.join(__testdir, 'list')
        __bothdir = os.path.join(__testdir, 'both')
        __archive = os.path.join(__testdir, 'custom-conf-filelist-zip.zip')
        __resultconffile = os.path.join(__testdir, 'conf', 'custom-conf-filelist-zip.conf')
        __resultlistfile = os.path.join(__testdir, 'list', 'custom-conf-filelist-zip.list')
        __resultbothconffile = os.path.join(__testdir, 'both', 'custom-conf-filelist-zip.conf')
        __resultbothlistfile = os.path.join(__testdir, 'both', 'custom-conf-filelist-zip.list')
        if not os.path.exists(__confdir):
            os.mkdir(__confdir)
        if not os.path.exists(__listdir):
            os.mkdir(__listdir)
        if not os.path.exists(__bothdir):
            os.mkdir(__bothdir)
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-zip.conf')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-zip.conf'))
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-zip.list')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-zip.list'))
        if os.path.exists(__resultconffile):
            remove(__resultconffile)
        if os.path.exists(__resultlistfile):
            remove(__resultlistfile)
        if os.path.exists(__resultbothconffile):
            remove(__resultbothconffile)
        if os.path.exists(__resultbothlistfile):
            remove(__resultbothlistfile)
        if 'PYTHONEXE' in environ:
            __retcode1 = subprocess.call([PYTHONEXE, EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode1 = subprocess.call([EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode2 = subprocess.call([PYTHONEXE, EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode2 = subprocess.call([EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode3 = subprocess.call([PYTHONEXE, EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode3 = subprocess.call([EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        if __retcode1 != 0 and __retcode2 != 0 and __retcode3 != 0:
            __queue.put('{} - {}return code:{} {} {}'.format(__testname, KOMSG, str(__retcode1), str(__retcode2), str(__retcode3)))
        else:
            if not os.path.exists(__resultconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultconffile))
            elif not os.path.exists(__resultlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultlistfile))
            elif not os.path.exists(__resultbothconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothconffile))
            elif not os.path.exists(__resultbothlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothlistfile))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_custom_conf_filelist_tree:
    '''Test to define a custom location to write conf and listfile files for a tree of files'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/custom-conf-filelist-tree')
        __confdir = os.path.join(__testdir, 'conf')
        __listdir = os.path.join(__testdir, 'list')
        __bothdir = os.path.join(__testdir, 'both')
        __archive = os.path.join(__testdir, 'custom-conf-filelist-tree')
        __resultconffile = os.path.join(__testdir, 'conf', 'custom-conf-filelist-tree.conf')
        __resultlistfile = os.path.join(__testdir, 'list', 'custom-conf-filelist-tree.list')
        __resultbothconffile = os.path.join(__testdir, 'both', 'custom-conf-filelist-tree.conf')
        __resultbothlistfile = os.path.join(__testdir, 'both', 'custom-conf-filelist-tree.list')
        if not os.path.exists(__confdir):
            os.mkdir(__confdir)
        if not os.path.exists(__listdir):
            os.mkdir(__listdir)
        if not os.path.exists(__bothdir):
            os.mkdir(__bothdir)
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-tree.conf')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-tree.conf'))
        if os.path.exists(os.path.join(__testdir, 'custom-conf-filelist-tree.list')):
            remove(os.path.join(__testdir, 'custom-conf-filelist-tree.list'))
        if os.path.exists(__resultconffile):
            remove(__resultconffile)
        if os.path.exists(__resultlistfile):
            remove(__resultlistfile)
        if os.path.exists(__resultbothconffile):
            remove(__resultbothconffile)
        if os.path.exists(__resultbothlistfile):
            remove(__resultbothlistfile)
        if 'PYTHONEXE' in environ:
            __retcode1 = subprocess.call([PYTHONEXE, EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode1 = subprocess.call([EXE, '-C', os.path.join(__testdir, 'conf/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode2 = subprocess.call([PYTHONEXE, EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode2 = subprocess.call([EXE, '-L', os.path.join(__testdir, 'list/'), OPTHASHES, OPTFULLGEN, __archive])
        if 'PYTHONEXE' in environ:
            __retcode3 = subprocess.call([PYTHONEXE, EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode3 = subprocess.call([EXE, '-O', os.path.join(__testdir, 'both/'), OPTHASHES, OPTFULLGEN, __archive])
        if __retcode1 != 0 and __retcode2 != 0 and __retcode3 != 0:
            __queue.put('{} - {}return code:{} {} {}'.format(__testname, KOMSG, str(__retcode1), str(__retcode2), str(__retcode3)))
        else:
            if not os.path.exists(__resultconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultconffile))
            elif not os.path.exists(__resultlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultlistfile))
            elif not os.path.exists(__resultbothconffile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothconffile))
            elif not os.path.exists(__resultbothlistfile):
                __queue.put('{} - {}missing {}'.format(__testname, KOMSG, __resultbothlistfile))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_hashtype_option:
    '''Test the hashtype option'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/hashtype-option')
        __targzdir = os.path.join(__testdir, 'tar-gz')
        __gzipdir = os.path.join(__testdir, 'gzip')
        __bzip2dir = os.path.join(__testdir, 'bzip2')
        __lzmadir = os.path.join(__testdir, 'lzma')
        __treedir = os.path.join(__testdir, 'tree')
        __zipdir = os.path.join(__testdir, 'zip')
        __resulttargzfile = os.path.join(__targzdir, 'hashtype-option.list')
        __resultgzipfile = os.path.join(__gzipdir, 'hashtype-option.list')
        __resultbzip2file = os.path.join(__bzip2dir, 'hashtype-option.list')
        __resultlzmafile = os.path.join(__lzmadir, 'hashtype-option.list')
        __resultzipfile = os.path.join(__zipdir, 'hashtype-option.list')
        __resulttreefile = os.path.join(__treedir, 'hashtype-option.list')
        __targzarchive = os.path.join(__targzdir, 'hashtype-option.tar.gz')
        __gziparchive = os.path.join(__gzipdir, 'hashtype-option.gz')
        __bzip2archive = os.path.join(__bzip2dir, 'hashtype-option.bz2')
        __lzmaarchive = os.path.join(__lzmadir, 'hashtype-option.xz')
        __treearchive = os.path.join(__treedir, 'hashtype-option')
        __ziparchive = os.path.join(__zipdir, 'hashtype-option.zip')
        if os.path.exists(__resulttargzfile):
            remove(__resulttargzfile)
        if os.path.exists(__resultgzipfile):
            remove(__resultgzipfile)
        if os.path.exists(__resultbzip2file):
            remove(__resultbzip2file)
        if os.path.exists(__resultlzmafile):
            remove(__resultlzmafile)
        if os.path.exists(__resultzipfile):
            remove(__resultzipfile)
        if os.path.exists(__resulttreefile):
            remove(__resulttreefile)
        # sha1
        if 'PYTHONEXE' in environ:
            __retcode1 = subprocess.call([PYTHONEXE, EXE, '-O', __targzdir, OPTHASHTYPE, 'sha1', OPTHASHES, OPTFULLGEN, __targzarchive])
        else:
            __retcode1 = subprocess.call([EXE, '-O', __targzdir, OPTHASHTYPE, 'sha1', OPTHASHES, OPTFULLGEN, __targzarchive])
        # sha224
        if 'PYTHONEXE' in environ:
            __retcode2 = subprocess.call([PYTHONEXE, EXE, '-O', __gzipdir, OPTHASHTYPE, 'sha224', OPTHASHES, OPTFULLGEN, __gziparchive])
        else:
            __retcode2 = subprocess.call([EXE, '-O', __gzipdir, OPTHASHTYPE, 'sha224', OPTHASHES, OPTFULLGEN, __gziparchive])
        # sha256
        if 'PYTHONEXE' in environ:
            __retcode3 = subprocess.call([PYTHONEXE, EXE, '-O', __bzip2dir, OPTHASHTYPE, 'sha256', OPTHASHES, OPTFULLGEN, __bzip2archive])
        else:
            __retcode3 = subprocess.call([EXE, '-O', __bzip2dir, OPTHASHTYPE, 'sha256', OPTHASHES, OPTFULLGEN, __bzip2archive])
        # sha384
        if 'PYTHONEXE' in environ:
            __retcode4 = subprocess.call([PYTHONEXE, EXE, '-O', __lzmadir, OPTHASHTYPE, 'sha384', OPTHASHES, OPTFULLGEN, __lzmaarchive])
        else:
            __retcode4 = subprocess.call([EXE, '-O', __lzmadir, OPTHASHTYPE, 'sha384', OPTHASHES, OPTFULLGEN, __lzmaarchive])
        # sha512
        if 'PYTHONEXE' in environ:
            __retcode5 = subprocess.call([PYTHONEXE, EXE, '-O', __zipdir, OPTHASHTYPE, 'sha512', OPTHASHES, OPTFULLGEN, __ziparchive])
        else:
            __retcode5 = subprocess.call([EXE, '-O', __zipdir, OPTHASHTYPE, 'sha512', OPTHASHES, OPTFULLGEN, __ziparchive])
        # sha1 again
        if 'PYTHONEXE' in environ:
            __retcode6 = subprocess.call([PYTHONEXE, EXE, '-O', __treedir, OPTHASHTYPE, 'sha1', OPTHASHES, OPTFULLGEN, __treearchive])
        else:
            __retcode6 = subprocess.call([EXE, '-O', __treedir, OPTHASHTYPE, 'sha1', OPTHASHES, OPTFULLGEN, __treearchive])
        if __retcode1 != 0 and __retcode2 != 0 and __retcode3 != 0 and __retcode4 != 0 and __retcode5 != 0:
            __queue.put('{} - {}return code:{} {} {} {} {}'.format(__testname, KOMSG, str(__retcode1), str(__retcode2), str(__retcode3), str(__retcode4), str(__retcode5), str(__retcode6)))
        else:
            __returnok = True
            for __test in [(__resulttargzfile, 'sha1'), (__resultgzipfile, 'sha224'), (__resultbzip2file, 'sha256'), (__resultlzmafile, 'sha384'), (__resultzipfile, 'sha512'), (__resulttreefile, 'sha1')]:
                with open(__test[0], 'r') as __file: 
                    __content = __file.read()
                    if __test[1] not in __content:
                        __returnok = False
                        __queue.put('{} - {} - {} not in {}'.format(__testname, KOMSG, __test[0], __test[1]))
            if __returnok:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_exceptions_file_option:
    '''Test the exceptions file option'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/exceptions-file-option')
        __targzdir = os.path.join(__testdir, 'tar-gz')
        __zipdir = os.path.join(__testdir, 'zip')
        __gzipdir = os.path.join(__testdir, 'gzip')
        __bzip2dir = os.path.join(__testdir, 'bzip2')
        __lzmadir = os.path.join(__testdir, 'lzma')
        __treedir = os.path.join(__testdir, 'tree')
        __resulttargzfile = os.path.join(__targzdir, 'exceptions-file-option.list')
        __resultzipfile = os.path.join(__zipdir, 'exceptions-file-option.list')
        __resultgzipfile = os.path.join(__gzipdir, 'exceptions-file-option.list')
        __resultbzip2file = os.path.join(__bzip2dir, 'exceptions-file-option.list')
        __resultlzmafile = os.path.join(__lzmadir, 'exceptions-file-option.list')
        __resulttreefile = os.path.join(__treedir, 'exceptions-file-option.list')
        __targzexceptionsfile = os.path.join(__targzdir, 'targzexceptionsfile')
        __zipexceptionsfile = os.path.join(__zipdir, 'zipexceptionsfile')
        __gzipexceptionsfile = os.path.join(__gzipdir, 'gzipexceptionsfile')
        __bzip2exceptionsfile = os.path.join(__bzip2dir, 'bzip2exceptionsfile')
        __lzmaexceptionsfile = os.path.join(__lzmadir, 'lzmaexceptionsfile')
        __treeexceptionsfile = os.path.join(__treedir, 'treeexceptionsfile')
        __targzarchive = os.path.join(__targzdir, 'exceptions-file-option.tar.gz')
        __ziparchive = os.path.join(__zipdir, 'exceptions-file-option.zip')
        __gziparchive = os.path.join(__gzipdir, 'exceptions-file-option.gz')
        __bzip2archive = os.path.join(__bzip2dir, 'exceptions-file-option.bz2')
        __lzmaarchive = os.path.join(__lzmadir, 'exceptions-file-option.xz')
        __treearchive = os.path.join(__treedir, 'exceptions-file-option')
        if os.path.exists(__resulttargzfile):
            remove(__resulttargzfile)
        if os.path.exists(__resultzipfile):
            remove(__resultzipfile)
        if os.path.exists(__resultgzipfile):
            remove(__resultgzipfile)
        if os.path.exists(__resultbzip2file):
            remove(__resultbzip2file)
        if os.path.exists(__resultlzmafile):
            remove(__resultlzmafile)
        if os.path.exists(__resulttreefile):
            remove(__resulttreefile)
        # tar.gz
        if 'PYTHONEXE' in environ:
            __retcode1 = subprocess.call([PYTHONEXE, EXE, '-O', __targzdir, OPTEXCEPTIONSFILE, __targzexceptionsfile, OPTFULLGEN, __targzarchive])
        else:
            __retcode1 = subprocess.call([EXE, '-O', __targzdir, OPTEXCEPTIONSFILE, __targzexceptionsfile, OPTFULLGEN, __targzarchive])
        # zip
        if 'PYTHONEXE' in environ:
            __retcode2 = subprocess.call([PYTHONEXE, EXE, '-O', __zipdir, OPTEXCEPTIONSFILE, __zipexceptionsfile, OPTFULLGEN, __ziparchive])
        else:
            __retcode2 = subprocess.call([EXE, '-O', __zipdir, OPTEXCEPTIONSFILE, __zipexceptionsfile, OPTFULLGEN, __ziparchive])
        # gzip
        if 'PYTHONEXE' in environ:
            __retcode3 = subprocess.call([PYTHONEXE, EXE, '-O', __gzipdir, OPTEXCEPTIONSFILE, __gzipexceptionsfile, OPTFULLGEN, __gziparchive])
        else:
            __retcode3 = subprocess.call([EXE, '-O', __gzipdir, OPTEXCEPTIONSFILE, __gzipexceptionsfile, OPTFULLGEN, __gziparchive])
        # bzip2
        if 'PYTHONEXE' in environ:
            __retcode4 = subprocess.call([PYTHONEXE, EXE, '-O', __bzip2dir, OPTEXCEPTIONSFILE, __bzip2exceptionsfile, OPTFULLGEN, __bzip2archive])
        else:
            __retcode4 = subprocess.call([EXE, '-O', __bzip2dir, OPTEXCEPTIONSFILE, __bzip2exceptionsfile, OPTFULLGEN, __bzip2archive])
        # lzma
        if 'PYTHONEXE' in environ:
            __retcode5 = subprocess.call([PYTHONEXE, EXE, '-O', __lzmadir, OPTEXCEPTIONSFILE, __lzmaexceptionsfile, OPTFULLGEN, __lzmaarchive])
        else:
            __retcode5 = subprocess.call([EXE, '-O', __lzmadir, OPTEXCEPTIONSFILE, __lzmaexceptionsfile, OPTFULLGEN, __lzmaarchive])
        # tree
        if 'PYTHONEXE' in environ:
            __retcode6 = subprocess.call([PYTHONEXE, EXE, '-O', __treedir, OPTEXCEPTIONSFILE, __treeexceptionsfile, OPTFULLGEN, __treearchive])
        else:
            __retcode6 = subprocess.call([EXE, '-O', __treedir, OPTEXCEPTIONSFILE, __treeexceptionsfile, OPTFULLGEN, __treearchive])
        if __retcode1 != 0 and __retcode2 != 0 and __retcode3 != 0 and __retcode4 != 0 and __retcode5 != 0 and __retcode6 != 0 :
            __queue.put('{} - {}return code:{} {} {} {} {}'.format(__testname, KOMSG, str(__retcode1), str(__retcode2), str(__retcode3), str(__retcode4), str(__retcode5), str(__retcode6)))
        else:
            __returnok = True
            for __test in [(__resulttargzfile, 'sha1'), (__resultgzipfile, 'sha224'), (__resultbzip2file, 'sha384'), (__resultlzmafile, 'sha512'), (__resultzipfile, 'sha224'), (__resulttreefile, 'sha1')]:
                with open(__test[0], 'r') as __file: 
                    __content = __file.read()
                    if __test[1] not in __content:
                        __returnok = False
                        __queue.put('{} - {} - {} not in {}'.format(__testname, KOMSG, __test[0], __test[1]))
            if __returnok:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_generate_list_to_check_uname_in_tar_gz_archive:
    '''Generate a list of files to check that uname in tar.gz archive is written'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/check-uname-tar-gz')
        __archive = os.path.join(__testdir, 'check-uname-tar-gz.tar.gz')
        __resultfile = os.path.join(__testdir, 'check-uname-tar-gz.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__resultfile, 'r') as __file:
                    if ' owner|' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_to_check_gname_in_tar_gz_archive:
    '''Generate a list of files to check that gname in tar.gz archive is written'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/check-gname-tar-gz')
        __archive = os.path.join(__testdir, 'check-gname-tar-gz.tar.gz')
        __resultfile = os.path.join(__testdir, 'check-gname-tar-gz.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__resultfile, 'r') as __file:
                    if ' group|' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_to_check_uname_in_tree:
    '''Generate a list of files to check that uname in tree is written'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/check-uname-tree')
        __archive = os.path.join(__testdir, 'check-uname-tree')
        __resultfile = os.path.join(__testdir, 'check-uname-tree.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__resultfile, 'r') as __file:
                    if ' owner|' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_list_to_check_gname_in_tree:
    '''Generate a list of files to check that gname in tree is written'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/check-gname-tree')
        __archive = os.path.join(__testdir, 'check-gname-tree')
        __resultfile = os.path.join(__testdir, 'check-gname-tree.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTHASHES, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTHASHES, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly modified list of files with the new delimiter
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call([PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            else:
                __retcode = subprocess.call([EXE, OPTCONFIG, __testdir, OPTLOG, __output])
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                with open(__resultfile, 'r') as __file:
                    if ' group|' in __file.read():
                        __queue.put('{} - {}'.format(__testname, OKMSG))
                    else:
                        __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))

class Test_generate_confs_for_stream_from_tar_gz:
    '''Generate configuration files for a stream from a tar.gz file'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/conf-files-from-tar-gz')
        __archive = os.path.join(__testdir, 'conf-files-from-tar-gz.tar.gz')
        __resultconffile = os.path.join(__testdir, 'conf-files-from-tar-gz.conf')
        __resultlistfile = os.path.join(__testdir, 'conf-files-from-tar-gz.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call('cat {} | {} {} {} {}'.format(__archive, PYTHONEXE, EXE, OPTFULLGEN, __archive), shell=True)
        else:
            __retcode = subprocess.call('cat {} | {} {} {}'.format(__archive, EXE, OPTFULLGEN, __archive), shell=True)
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            with open(__resultconffile, 'r') as __file:
                if '[main]\nname=conf-files-from-tar-gz\ntype=archive' in __file.read():
                    test1 = True
                else:
                    test1 = False
            with open(__resultlistfile, 'r') as __file:
                if '[files]' in __file.read():
                    test2 = True
                else:
                    test2 = False
            if not test1 or not test2:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_generate_and_check_for_stream_from_tar_gz:
    '''Generate configuration files and after check the archive for a tar.gz stream'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/generate-and-check-tar-stream-from-tar-gz')
        __archive = os.path.join(__testdir, 'generate-and-check-tar-stream-from-tar-gz.tar.gz')
        __resultconffile = os.path.join(__testdir, 'generate-and-check-tar-stream-from-tar-gz.conf')
        __resultlistfile = os.path.join(__testdir, 'generate-and-check-tar-stream-from-tar-gz.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call('cat {} | {} {} {} {}'.format(__archive, PYTHONEXE, EXE, OPTFULLGEN, __archive), shell=True)
        else:
           __retcode = subprocess.call('cat {} | {} {} {}'.format(__archive, EXE, OPTFULLGEN, __archive), shell=True)
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            # check now the newly created configuration files
            if 'PYTHONEXE' in environ:
                __retcode = subprocess.call('cat {} | {} {} {} {} {} {}'.format(__archive, PYTHONEXE, EXE, OPTCONFIG, __testdir, OPTLOG, __output), shell=True)
            else:
                __retcode = subprocess.call('cat {} | {} {} {} {} {}'.format(__archive, EXE, OPTCONFIG, __testdir, OPTLOG, __output), shell=True)
            if __retcode != 0:
                __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_configuration_name_option_with_tar_gz:
    '''Generate configuration files and check if switching configuration names was successful with tar.gz archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/configuration-name-option-with-tar-gz')
        __archive = os.path.join(__testdir, 'configuration-name-option-with-tar-gz.tar.gz')
        __newname = 'newname'
        __resultconffile = os.path.join(__testdir, 'newname.conf')
        __resultlistfile = os.path.join(__testdir, 'newname.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call('{} {} {} {} {} {}'.format(PYTHONEXE, EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        else:
           __retcode = subprocess.call('{} {} {} {} {}'.format(EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if os.path.exists(__resultconffile):
                test1 = True
            else:
                test1 = False
            if os.path.exists(__resultlistfile):
                test2 = True
            else:
                test2 = False
            with open(__resultconffile, 'r') as __file:
                if '[main]\nname=newname' in __file.read():
                    test3 = True
                else:
                    test3 = False
            if not test1 or not test2 or not test3:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_configuration_name_option_with_zip:
    '''Generate configuration files and check if switching configuration names was successful with zip archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/configuration-name-option-with-zip')
        __archive = os.path.join(__testdir, 'configuration-name-option-with-zip.zip')
        __newname = 'newname'
        __resultconffile = os.path.join(__testdir, 'newname.conf')
        __resultlistfile = os.path.join(__testdir, 'newname.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call('{} {} {} {} {} {}'.format(PYTHONEXE, EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        else:
           __retcode = subprocess.call('{} {} {} {} {}'.format(EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if os.path.exists(__resultconffile):
                test1 = True
            else:
                test1 = False
            if os.path.exists(__resultlistfile):
                test2 = True
            else:
                test2 = False
            with open(__resultconffile, 'r') as __file:
                if '[main]\nname=newname' in __file.read():
                    test3 = True
                else:
                    test3 = False
            if not test1 or not test2 or not test3:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_configuration_name_option_with_tree:
    '''Generate configuration files and check if switching configuration names was successful with a tree of files'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/configuration-name-option-with-tree')
        __archive = os.path.join(__testdir, 'configuration-name-option-with-tree')
        __newname = 'newname'
        __resultconffile = os.path.join(__testdir, 'newname.conf')
        __resultlistfile = os.path.join(__testdir, 'newname.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call('{} {} {} {} {} {}'.format(PYTHONEXE, EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        else:
           __retcode = subprocess.call('{} {} {} {} {}'.format(EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if os.path.exists(__resultconffile):
                test1 = True
            else:
                test1 = False
            if os.path.exists(__resultlistfile):
                test2 = True
            else:
                test2 = False
            with open(__resultconffile, 'r') as __file:
                if '[main]\nname=newname' in __file.read():
                    test3 = True
                else:
                    test3 = False
            if not test1 or not test2 or not test3:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_configuration_name_option_with_gzip:
    '''Generate configuration files and check if switching configuration names was successful with gzip archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/configuration-name-option-with-gzip')
        __archive = os.path.join(__testdir, 'configuration-name-option-with-gzip.gz')
        __newname = 'newname'
        __resultconffile = os.path.join(__testdir, 'newname.conf')
        __resultlistfile = os.path.join(__testdir, 'newname.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call('{} {} {} {} {} {}'.format(PYTHONEXE, EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        else:
           __retcode = subprocess.call('{} {} {} {} {}'.format(EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if os.path.exists(__resultconffile):
                test1 = True
            else:
                test1 = False
            if os.path.exists(__resultlistfile):
                test2 = True
            else:
                test2 = False
            with open(__resultconffile, 'r') as __file:
                if '[main]\nname=newname' in __file.read():
                    test3 = True
                else:
                    test3 = False
            if not test1 or not test2 or not test3:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_configuration_name_option_with_bzip2:
    '''Generate configuration files and check if switching configuration names was successful with bzip2 archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/configuration-name-option-with-bzip2')
        __archive = os.path.join(__testdir, 'configuration-name-option-with-bzip2.bz2')
        __newname = 'newname'
        __resultconffile = os.path.join(__testdir, 'newname.conf')
        __resultlistfile = os.path.join(__testdir, 'newname.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call('{} {} {} {} {} {}'.format(PYTHONEXE, EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        else:
           __retcode = subprocess.call('{} {} {} {} {}'.format(EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if os.path.exists(__resultconffile):
                test1 = True
            else:
                test1 = False
            if os.path.exists(__resultlistfile):
                test2 = True
            else:
                test2 = False
            with open(__resultconffile, 'r') as __file:
                if '[main]\nname=newname' in __file.read():
                    test3 = True
                else:
                    test3 = False
            if not test1 or not test2 or not test3:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_configuration_name_option_with_lzma:
    '''Generate configuration files and check if switching configuration names was successful with lzma archive'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/configuration-name-option-with-lzma')
        __archive = os.path.join(__testdir, 'configuration-name-option-with-lzma.xz')
        __newname = 'newname'
        __resultconffile = os.path.join(__testdir, 'newname.conf')
        __resultlistfile = os.path.join(__testdir, 'newname.list')
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call('{} {} {} {} {} {}'.format(PYTHONEXE, EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        else:
           __retcode = subprocess.call('{} {} {} {} {}'.format(EXE, OPTCONFNAME, __newname, OPTFULLGEN, __archive), shell=True)
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if os.path.exists(__resultconffile):
                test1 = True
            else:
                test1 = False
            if os.path.exists(__resultlistfile):
                test2 = True
            else:
                test2 = False
            with open(__resultconffile, 'r') as __file:
                if '[main]\nname=newname' in __file.read():
                    test3 = True
                else:
                    test3 = False
            if not test1 or not test2 or not test3:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))

class Test_configuration_name_option_and_conf_list_output_with_tar_gz:
    '''Generate configuration files and check if switching configuration names was successful with tar.gz archive.
       This test also uses the output-conf-dir and -output-list-dir options.'''
    def __init__(self, q):
        __queue = q
        __res = True
        __testname = self.__class__.__name__
        __testdir = os.path.join(ABSPATH, 'functional-tests/configuration-name-option-and-conf-list-ouput-option-with-tar-gz')
        __archive = os.path.join(__testdir, 'configuration-name-option-and-conf-list-ouput-option-with-tar-gz.tar.gz')
        __newname = 'newname2'
        __resultconffile = os.path.join(__testdir, 'conf/newname2.conf')
        if os.path.exists(__resultconffile):
            remove(__resultconffile)
        __resultconfdir = os.path.dirname(__resultconffile)
        if not os.path.exists(__resultconfdir):
            os.mkdir(__resultconfdir)
        __resultlistfile = os.path.join(__testdir, 'list/newname2.list')
        if os.path.exists(__resultlistfile):
            remove(__resultlistfile)
        __resultlistdir = os.path.dirname(__resultlistfile)
        if not os.path.exists(__resultlistdir):
            os.mkdir(__resultlistdir)
        __output = os.path.join(__testdir, 'a.out')
        if 'PYTHONEXE' in environ:
            __retcode = subprocess.call([PYTHONEXE, EXE, OPTOUTPUTCONFDIR, __resultconfdir, OPTOUTPUTLISTDIR, __resultlistdir, OPTCONFNAME, __newname, OPTFULLGEN, __archive])
        else:
            __retcode = subprocess.call([EXE, OPTOUTPUTCONFDIR, __resultconfdir, OPTOUTPUTLISTDIR, __resultlistdir, OPTCONFNAME, __newname, OPTFULLGEN, __archive])
        if __retcode != 0:
            __queue.put('{} - {}return code:{}'.format(__testname, KOMSG, str(__retcode)))
        else:
            if os.path.exists(__resultconffile):
                test1 = True
            else:
                test1 = False
            if os.path.exists(__resultlistfile):
                test2 = True
            else:
                test2 = False
            with open(__resultconffile, 'r') as __file:
                if '[main]\nname=newname' in __file.read():
                    test3 = True
                else:
                    test3 = False
            if not test1 or not test2 or not test3:
                __queue.put('{} - {}value in result file not expected'.format(__testname, KOMSG))
            else:
                __queue.put('{} - {}'.format(__testname, OKMSG))


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

