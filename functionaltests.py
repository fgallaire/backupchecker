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
from os import linesep, environ
import subprocess
import os.path
import sys

import functionaltests

EXE = './brebis.py'
OPTCONFIG = '-c'
OPTLOG = '-l'
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

class Test1_file_missing_in_tar_gz(Main):
    '''Test if a file is missing in a tar.gz archive'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-tar-gz')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')


class Test2_file_missing_in_tar_bz2(Main):
    '''Test if a file is missing in a tar.bz2 archive'''
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-tar-bz2')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test3_file_missing_in_zip(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-zip')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test4_file_missing_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/file-missing-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file missing in')

class Test5_wrong_tar_gz_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test6_wrong_tar_bz2_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test7_wrong_zip_archive_mode(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-mode')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test8_wrong_tar_gz_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-uid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test9_wrong_tar_bz2_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-uid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test10_wrong_zip_archive_uid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-uid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test11_wrong_tar_gz_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test12_wrong_tar_bz2_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test13_wrong_zip_archive_gid(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-gid')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test14_wrong_tar_gz_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test15_wrong_tar_gz_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha1-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test16_wrong_tar_gz_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test17_wrong_tar_gz_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test18_wrong_tar_gz_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test19_wrong_tar_gz_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-gz-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test20_wrong_tar_bz2_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test21_wrong_tar_bz2_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha1-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test22_wrong_tar_bz2_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test23_wrong_tar_bz2_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test24_wrong_tar_bz2_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test25_wrong_tar_bz2_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-tar-bz2-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test26_wrong_zip_archive_md5_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-md5-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test27_wrong_zip_archive_sha1_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha1-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test28_wrong_zip_archive_sha224_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha224-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test29_wrong_zip_archive_sha256_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha256-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test30_wrong_zip_archive_sha384_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha384-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test31_wrong_zip_archive_sha512_hash(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-zip-archive-sha512-hash')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test32_wrong_file_uid_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test33_wrong_file_uid_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')


class Test33_wrong_file_uid_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test34_wrong_file_uid_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-uid-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected uid')

class Test35_wrong_file_gid_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test36_wrong_file_gid_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test37_wrong_file_gid_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test37_wrong_file_gid_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-gid-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected gid')

class Test38_unexpected_file_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test39_unexpected_file_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test40_unexpected_file_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test41_unexpected_file_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/unexpected-file-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 unexpected file')

class Test42_wrong_file_md5_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')


class Test43_wrong_file_sha1_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test44_wrong_file_sha224_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test45_wrong_file_sha256_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test46_wrong_file_sha384_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test47_wrong_file_sha512_hash_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test48_wrong_file_md5_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test49_wrong_file_sha1_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test50_wrong_file_sha224_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test51_wrong_file_sha256_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test52_wrong_file_sha384_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test53_wrong_file_sha512_hash_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test54_wrong_file_md5_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test55_wrong_file_sha1_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test56_wrong_file_sha224_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test57_wrong_file_sha256_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test58_wrong_file_sha384_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')


class Test59_wrong_file_sha512_hash_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test60_wrong_file_md5_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-md5-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test61_wrong_file_sha1_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha1-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test62_wrong_file_sha224_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha224-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test63_wrong_file_sha256_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha256-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test64_wrong_file_sha384_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha384-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test65_wrong_file_sha512_hash_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-sha512-hash-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected hash')

class Test66_wrong_file_mode_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-mode-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test67_wrong_file_mode_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-mode-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test68_wrong_file_mode_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-mode-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test69_wrong_file_mode_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-mode-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected mode')

class Test70_wrong_file_type_f_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-f-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test71_wrong_file_type_f_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-f-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test72_wrong_file_type_f_in_zip_archive(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-f-in-zip-archive')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected type')


class Test72_wrong_file_type_f_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-f-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test73_wrong_file_type_d_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-d-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test74_wrong_file_type_d_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-d-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test75_wrong_file_type_d_in_zip_archive(Main):
   def __init__(self, q):
       self._queue = q
       self._testname = self.__class__.__name__
       self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-d-in-zip-archive')
       self._resultfile = os.path.join(self._testdir, 'a.out')
       self._main('1 file with unexpected type')

class Test76_wrong_file_type_d_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/wrong-file-type-d-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected type')

class Test77_corrupted_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('data corruption')

class Test78_corrupted_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('data corruption')

class Test79_corrupted_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/corrupted-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('data corruption')

class Test80_two_confs_with_the_same_name(Main):
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

class Test81_expected_file_greater_than_file_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test82_expected_file_greater_than_file_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test83_expected_file_greater_than_file_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test84_expected_file_greater_than_file_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-greater-than-file-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file smaller than expected')
            
class Test85_expected_file_smaller_than_file_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test86_expected_file_smaller_than_file_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test87_expected_file_smaller_than_file_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test88_expected_file_smaller_than_file_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-smaller-than-file-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file bigger than expected')
            
class Test89_expected_file_not_equals_file_in_tar_gz_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-tar-gz-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test90_expected_file_not_equals_file_in_tar_bz2_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-tar-bz2-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test91_expected_file_not_equals_file_in_zip_archive(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-zip-archive')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test92_expected_file_not_equals_file_in_tree(Main):
    def __init__(self, q):
        self._queue = q
        self._testname = self.__class__.__name__
        self._testdir = os.path.join(ABSPATH, 'functional-tests/expected-file-not-equals-file-in-tree')
        self._resultfile = os.path.join(self._testdir, 'a.out')
        self._main('1 file with unexpected size')
            
class Test93_mixing_dir_path_and_archive_type_in_conf(Main):
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


def extract_key(key):
    return int(key.split('_')[0][4:])

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
        print(linesep.join(sorted(koresults,key=functionaltests.extract_key)))
        sys.exit(1)
    else:
        print(linesep.join(sorted(results,key=functionaltests.extract_key)))
