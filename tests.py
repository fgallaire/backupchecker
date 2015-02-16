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

import argparse
import bz2
import gzip
import logging
import os
import os.path
import stat
import sys
import tarfile
import unittest
import zipfile

import backupchecker.applogger
import backupchecker.archiveinfomsg
import backupchecker.checkbackups.checkarchive
import backupchecker.checkbackups.checkbackups
import backupchecker.checkbackups.checkbzip2
import backupchecker.checkbackups.checkgzip
import backupchecker.checkbackups.checklzma
import backupchecker.checkhashes
import backupchecker.checkbackups.checktar
import backupchecker.checkbackups.checktree
import backupchecker.checkbackups.checkzip
import backupchecker.cliparse
import backupchecker.configurations
from backupchecker.expectedvalues import ExpectedValues
import backupchecker.generatelist.generatelistfortar
import backupchecker.generatelist.generatelistforbzip2
import backupchecker.listtype
import backupchecker.main

# !! logging module uses a single logger for the whole file
TESTLOG = 'tests/testlog'
DEFAULTDELIMITER = '|'

# mock the object produced by argparse, useful for lots of tests below
class Options:
    '''Mock the object produced by argparse, useful for lots of unittests'''
    def __init__(self):
        self.delimiter = DEFAULTDELIMITER

class MyDict(dict):
    '''mock object'''
    pass

class TestApp(unittest.TestCase):

    def test_applogger(self):
        '''Test the AppLoggerclass'''
        backupchecker.applogger.AppLogger(TESTLOG)
        self.assertEqual(True, str(logging.getLogger('applogger')).startswith('<logging.Logger object at'))
        
    def test_checkbackup(self):
        '''Test the CheckBackup class'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(_logfile)
        backupchecker.checkbackups.checkbackups.CheckBackups({'essai': {'path': 'tests/tar_gz_archive_content/essai.tar.gz', 'files_list': 'tests/tar_gz_archive_content/essai-list', 'type': 'archive','delimiter':''}, 'essai2': {'path': 'tests/tar_bz2_archive_content/titi.tar.bz2', 'files_list': 'tests/tar_bz2_archive_content/essai2-list', 'type': 'archive','delimiter':''}}, Options())
        with open(_logfile) as _res:
            self.assertIn('WARNING:root:1 file missing in tests/tar_gz_archive_content/essai.tar.gz: \nWARNING:root:essai/dir/titi\n', _res.read())

    def test_checktar_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        _missingfiles = []
        _missingfiles = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/tar_gz_archive_content/essai.tar.gz',
             'files_list':
                'tests/tar_gz_archive_content/essai-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_files
        self.assertEqual(_missingfiles, ['essai/dir/titi'])

    def test_checktar_missing_equality(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'essai/dir/toto')

    def test_checktar_missing_bigger_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'essai/titi')

    def test_checktar_missing_smaller_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'essai/dir/toutou')

    def test_checktree_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        __missing_files = []
        __missing_files = backupchecker.checkbackups.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree', 'delimiter': ''}, Options()).missing_files
        self.assertEqual(__missing_files, ['bar/toto'])

    def test_checktree_missing_equality(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality= []
        __missing_equality = backupchecker.checkbackups.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'foo1')

    def test_checktree_missing_bigger_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = backupchecker.checkbackups.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'foo2')

    def test_checktree_missing_smaller_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = backupchecker.checkbackups.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'bar/foo3')

#######################################################################################
#
# Testing the backupchecker/checkbackup/checkgzip module
#
#######################################################################################

    def test_checkgzip_missing_files(self):
        '''Check if the CheckGzip class returns a missing file'''
        _missing_files = []
        _missing_files = backupchecker.checkbackups.checkgzip.CheckGzip({'path':
            'tests/gzip/mygzip.gz',
             'files_list':
                'tests/gzip/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_files
        self.assertEqual(_missing_files, ['foo'])

    def test_checkgzip_missing_equality(self):
        '''Check if the CheckGzip class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = backupchecker.checkbackups.checkgzip.CheckGzip({'path':
            'tests/file_size/mygzip.gz',
             'files_list':
                'tests/file_size/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'mygzip')

    def test_checkgzip_missing_bigger_than(self):
        '''Check if the CheckGzip class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than= []
        __missing_bigger_than = backupchecker.checkbackups.checkgzip.CheckGzip({'path':
            'tests/file_size/missing-bigger-than/mygzip.gz',
             'files_list':
                'tests/file_size/missing-bigger-than/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'mygzip')

    def test_checkgzip_missing_smaller_than(self):
        '''Check if the CheckGzip class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than= []
        __missing_smaller_than = backupchecker.checkbackups.checkgzip.CheckGzip({'path':
            'tests/file_size/missing-smaller-than/mygzip.gz',
             'files_list':
                'tests/file_size/missing-smaller-than/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'mygzip')

#######################################################################################
#
# Testing the backupchecker/checkbackup/checklzma module
#
#######################################################################################

    def test_checklzma_missing_files(self):
        '''Check if the CheckLzma class returns a missing file'''
        _missing_files = []
        _missing_files = backupchecker.checkbackups.checklzma.CheckLzma({'path':
            'tests/lzma/mylzma.xz',
             'files_list':
                'tests/lzma/mylzma-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_files
        self.assertEqual(_missing_files, ['foo'])

#######################################################################################
#
# Testing the backupchecker/checkbackup/checkzip module
#
#######################################################################################

    def test_checkzip_missing_files(self):
        '''Check if the CheckZip class returns a missing file'''
        _missing_files = []
        _missing_files = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/zip/myzip.zip',
             'files_list':
                'tests/zip/myzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_files
        self.assertEqual(_missing_files, ['toto/bling'])

    def test_checkzip_missing_equality(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'myzip/titi')

    def test_checkzip_missing_bigger_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than= []
        __missing_bigger_than = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'myzip/foo/toto')

    def test_checkzip_missing_smaller_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than= []
        __missing_smaller_than = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'myzip/toutou')

#######################################################################################
#
# Testing the backupchecker/configurations module
#
#######################################################################################

    def test_configurations(self):
        '''Test the Configurations.configs attribute of the Configurations class'''
        __path = os.path.abspath('tests/test_conf/')
        __res = backupchecker.configurations.Configurations(__path).configs
        self.assertEqual({'essai': {'path': os.path.normpath(os.path.join(__path,'essai.tar.gz')), 'sha512': None, 'files_list': os.path.normpath(os.path.join(__path,'essai-list')), 'type': 'archive', 'delimiter': '|'}}, __res)

    def test_configurations_with_subdir(self):
        '''Test the Configurations.configs attribute of the Configurations class'''
        __path = os.path.abspath('tests/test_conf/subdir/')
        __res = backupchecker.configurations.Configurations(__path).configs
        self.assertEqual({'essai2': {'path': os.path.normpath(os.path.join(__path, 'toto/essai.tar.gz')), 'sha512': None, 'files_list': os.path.normpath(os.path.join(__path, 'toto/essai-list')), 'type': 'archive', 'delimiter': None}}, __res)

    def test_configurations_strip_gpg_header(self):
        '''Test the Configurations.configs attribute of the Configurations class'''
        __base = os.path.abspath('tests/test_conf_gpg/')
        __path = os.path.join(__base, 'archive.conf')
        __strippedfilepath = os.path.join(__base, 'result')
        __myobj = backupchecker.configurations.Configurations(__path)
        with open(__path) as __myfile:
            __newfile = __myobj.strip_gpg_header(__myfile, __path)
        with open(__strippedfilepath) as __good:
            __goodfile = __good.read()
        self.assertEqual(__newfile, __goodfile)

#######################################################################################
#
# Testing the backupchecker/expectedvalues module
#
#######################################################################################
    def test_expected_values(self):
        '''Check the ExpectedValues class'''
        __data, _ = ExpectedValues({'files_list':'tests/file_size/essai-list','delimiter':''}, Options()).data
        self.assertEqual([{'path':'essai/dir/toto', 'equals':536870912},
            {'path':'essai/titi','biggerthan':536870912},
            {'path':'essai/dir/toutou','smallerthan':19},
            {'path':'essai/dir/zozo'}], __data)

    def test_unexpected_files(self):
        '''Check if an unexpected file is identified'''
        __data, _ = ExpectedValues({'files_list':'tests/unexpected_files/files-list','delimiter':''}, Options()).data
        self.assertEqual([{'path':'foo/foo1'},{'path':'foo/foo2'},
            {'path':'foo/bar','unexpected':True}], __data)

    def test_extract_expected_uid_gid(self):
        '''Check the uid and gid of an expected file''' 
        __data, _ = ExpectedValues({'files_list':'tests/expected_uid_gid/files-list','delimiter':''}, Options()).data
        self.assertEqual([{'path':'foo/foo1', 'uid':1001, 'gid':1001}], __data)

    def test_compare_uid_gid(self):
        '''Compare the uid and the gid of a file in the archive
        and the expected one
        '''
        __uids = []
        __gids = []
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/expected_uid_gid/foo.tar.gz',
             'files_list':
                'tests/expected_uid_gid/files-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __uids = __myobj.mismatched_uids
        __gids = __myobj.mismatched_gids
        self.assertEqual((__uids[0],__gids[0]), (
        {'path':'foo/foo1','expecteduid':1001,'uid':1000},
        {'path':'foo/foo1','expectedgid':1001,'gid':1000}))

    def test_compare_uname_gname_tar_gz(self):
        '''Compare the uname and the gname of a file in the archive
        and the expected one
        '''
        __unames = []
        __gnames = []
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/expected_uname_gname/foo.tar.gz',
             'files_list':
                'tests/expected_uname_gname/files-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __unames = __myobj.mismatched_unames
        __gnames = __myobj.mismatched_gnames
        self.assertEqual((__unames[0],__gnames[0]), (
        {'path':'foo/foo1','expecteduname':'titi','uname':'chaica'},
        {'path':'foo/foo1','expectedgname':'titi','gname':'chaica'}))

    def test_compare_uname_gname_tree(self):
        '''Compare the uname and the gname of a file in the tree
        and the expected one
        '''
        __unames = []
        __gnames = []
        __myobj = backupchecker.checkbackups.checktree.CheckTree({'path':
            'tests/expected_uname_gname/foo',
             'files_list':
                'tests/expected_uname_gname/files-list',
             'type': 'tree', 'delimiter': ''}, Options())
        __unames = __myobj.mismatched_unames
        __gnames = __myobj.mismatched_gnames
        self.assertEqual((__unames[0],__gnames[0]), (
        {'path':'foo/foo1','expecteduname':'titi','uname':'chaica'},
        {'path':'foo/foo1','expectedgname':'titi','gname':'chaica'}))

    def test_extract_modes(self):
        '''Extract the expected file modes'''
        __data, _ = ExpectedValues({'files_list':'tests/expected_mode/files-list','delimiter':''}, Options()).data
        self.assertEqual([{'path':'foos/foo1', 'mode': '644'},
            {'path':'foos/foo2', 'mode': '755'},
            {'path':'foos/bar/foo3', 'mode': '4644'},
            {'path':'foos/bar', 'mode': '754'}], __data)

    def test_archive_compare_mode(self):
        '''Compare the mode of a file in the archive and the
        expected one
        '''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/expected_mode/foos.tar.gz',
             'files_list':
                'tests/expected_mode/files-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'foos/foo2','expectedmode':'755','mode':'754'},
        {'path':'foos/bar','expectedmode':'754','mode':'755'},
        {'path':'foos/bar/foo3','expectedmode':'4644','mode':'4600'},
        {'path':'foos/foo1','expectedmode':'644','mode':'744'}])

    def test_extract_types(self):
        '''Extract the expected file types'''
        __data, _ = ExpectedValues({'files_list':'tests/expected_type/files-list','delimiter':''}, Options()).data
        self.assertEqual([{'path':'foos/foo1', 'type': 'f'},
            {'path':'foos/foo2', 'type': 'c'},
            {'path':'foos/foo3', 'type': 'd'},
            {'path':'foos/foo4', 'type': 's'},
            {'path':'foos/foo5', 'type': 'b'},
            {'path':'foos/foo6', 'type': 'k'},
            {'path':'foos/foo7', 'type': 'o'}], __data)

    def test_archive_compare_type(self):
        '''Compare the type of a file in the archive and the
        expected one
        '''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/expected_type/foos.tar.gz',
             'files_list':
                'tests/expected_type/files-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __types = __myobj.mismatched_types
        self.assertEqual(__types, [
        {'path':'foos/foo3','expectedtype':'d','type':'f'},
        {'path':'foos/foo2','expectedtype':'c','type':'f'},
        {'path':'foos/foo4','expectedtype':'s','type':'f'},
        {'path':'foos/foo6','expectedtype':'k','type':'f'},
        {'path':'foos/foo1','expectedtype':'f','type':'d'},
        {'path':'foos/foo5','expectedtype':'b','type':'f'},
        {'path':'foos/foo7','expectedtype':'o','type':'f'}])

    def test_extract_hashes(self):
        '''Extract the expected file hashes'''
        __data, _ = ExpectedValues({'files_list':'tests/expected_hash/files-list','delimiter':''}, Options()).data
        self.assertEqual([{'hash': {'hashtype': 'md5', 
            'hashvalue': '3718422a0bf93f7fc46cff6b5e660ff8'},
            'path': 'foos/foo1'},
            {'hash': {'hashtype': 'sha1',
            'hashvalue': 'e0f58dcc57caad2182f701eb63f0c81f347d3fe5'},
            'path': 'foos/foo2'},
            {'hash': {'hashtype': 'sha224',
            'hashvalue': 'g3c1d88024b6e2e333cbf8bed96182a62fbafaf2aea6dd8b17639552'},
            'path': 'foos/foo3'},
            {'hash': {'hashtype': 'sha256',
            'hashvalue': '35a670af482f46a76f8033e05cca7a53a58456fa42ef47ea56ffd2b16e408863'},
            'path': 'foos/foo4'},
            {'hash': {'hashtype': 'sha384',
            'hashvalue': '744e19f5c4258a573400b5059747d88797b150c08456e406e6473bd777332c5f66afe66c5bf77820906b97961c124810'},
            'path': 'foos/foo5'},
            {'hash': {'hashtype': 'sha512',
            'hashvalue': 'c46dcb0f5124bd681cb5b91c812d2982efce703806026b1f9ffdeadf45c4128cd3e61fa939a0bc89af317e70d0d6c74b666edff9bd7ad9052cb8e7f42c8f7644'},
            'path': 'foos/foo6'}], 
            __data)

    def test_archive_tar_compare_hash(self):
        '''Compare the hash of a file in the tar archive and the
        expected one
        '''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/expected_hash/foos.tar.gz',
             'files_list':
                'tests/expected_hash/files-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __hashes = __myobj.mismatched_hashes
        self.assertEqual(__hashes, [
            {'path': 'foos/foo3', 
            'expectedhash': 'g3c1d88024b6e2e333cbf8bed96182a62fbafaf2aea6dd8b17639552',
            'hash':'f3c1d88024b6e2e333cbf8bed96182a62fbafaf2aea6dd8b17639552'},
            {'path': 'foos/foo2',
            'expectedhash': 'e0f58dcc57caad2182f701eb63f0c81f347d3fe5',
            'hash': 'd0f58dcc57caad2182f701eb63f0c81f347d3fe5'},
            {'path': 'foos/foo4',
            'expectedhash': '35a670af482f46a76f8033e05cca7a53a58456fa42ef47ea56ffd2b16e408863',
            'hash': '25a670af482f46a76f8033e05cca7a53a58456fa42ef47ea56ffd2b16e408863'},
            {'path': 'foos/foo6',
            'expectedhash': 'c46dcb0f5124bd681cb5b91c812d2982efce703806026b1f9ffdeadf45c4128cd3e61fa939a0bc89af317e70d0d6c74b666edff9bd7ad9052cb8e7f42c8f7644',
            'hash': 'b46dcb0f5124bd681cb5b91c812d2982efce703806026b1f9ffdeadf45c4128cd3e61fa939a0bc89af317e70d0d6c74b666edff9bd7ad9052cb8e7f42c8f7644'},
            {'path': 'foos/foo1',
            'expectedhash': '3718422a0bf93f7fc46cff6b5e660ff8',
            'hash': '2718422a0bf93f7fc46cff6b5e660ff8'},
            {'path': 'foos/foo5',
            'expectedhash': '744e19f5c4258a573400b5059747d88797b150c08456e406e6473bd777332c5f66afe66c5bf77820906b97961c124810',
            'hash': '644e19f5c4258a573400b5059747d88797b150c08456e406e6473bd777332c5f66afe66c5bf77820906b97961c124810'}])


    def test_zip_compare_hash(self):
        '''Compare the hash of a file in the zip archive and the
        expected one
        '''
        __myobj = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/expected_hash/bar.zip',
             'files_list':
                'tests/expected_hash/zip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __hashes = __myobj.mismatched_hashes
        self.assertEqual(__hashes, [
            {'path': 'bar/bar5', 
            'expectedhash': '65305af91a511f6d091237f97e5dbccd1427c6f48bcd509acd0a71938bfe9d708cfb93c3d163f96b328f6cabb80b0860',
            'hash':'55305af91a511f6d091237f97e5dbccd1427c6f48bcd509acd0a71938bfe9d708cfb93c3d163f96b328f6cabb80b0860'},
            {'path': 'bar/bar4',
            'expectedhash': 'd67f2596a1ef0893f176b0b68d6e1445a9acd5fda2f5a073f1318ff4b75e5b84',
            'hash': 'c67f2596a1ef0893f176b0b68d6e1445a9acd5fda2f5a073f1318ff4b75e5b84'},
            {'path': 'bar/bar6',
            'expectedhash': 'g0fc5b14ab8b242e4c6462deee58a0a10fabdb4bc792174fdeec92cd12df8d5a7a8fed9545e2c109b3cecd345d970afaea0183ea0dd19371913cb55b23b9fc2e',
            'hash': 'f0fc5b14ab8b242e4c6462deee58a0a10fabdb4bc792174fdeec92cd12df8d5a7a8fed9545e2c109b3cecd345d970afaea0183ea0dd19371913cb55b23b9fc2e'},
            {'path': 'bar/bar3',
            'expectedhash': '33975be818906ec2228074d2a4438ef8f78ec33792aac4d037ad8f95',
            'hash': '23975be818906ec2228074d2a4438ef8f78ec33792aac4d037ad8f95'},
            {'path': 'bar/bar1',
            'expectedhash': '9151b18e6dd21a734890b56b5a15d24b',
            'hash': '8151b18e6dd21a734890b56b5a15d24b'},
            {'path': 'bar/bar2',
            'expectedhash': '3676c9d706eb6f6b02eb5d67ba86a9b3e855c13d',
            'hash': '2676c9d706eb6f6b02eb5d67ba86a9b3e855c13d'}])

    def test_gzip_compare_hash(self):
        '''Compare the hash of a file in the gzip archive and the
        expected one
        '''
        __myobj = backupchecker.checkbackups.checkgzip.CheckGzip({'path':
            'tests/expected_hash/bar.gz',
             'files_list':
                'tests/expected_hash/gzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __hashes = __myobj.mismatched_hashes
        self.assertEqual(__hashes, [
            {'path': 'bar',
            'expectedhash': 'ede',
            'hash': 'ede69eff9660689e65c5e47bb849f152'}])

    def test_lzma_compare_hash(self):
        '''Compare the hash of a file in the lzma archive and the
        expected one
        '''
        __myobj = backupchecker.checkbackups.checklzma.CheckLzma({'path':
            'tests/expected_hash/bar.xz',
             'files_list':
                'tests/expected_hash/lzma-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __hashes = __myobj.mismatched_hashes
        self.assertEqual(__hashes, [
            {'path': 'bar',
            'expectedhash': 'ede',
            'hash': '39fe9ceedb3aac1755142e7f425a5961'}])

    def test_bzip2_compare_hash(self):
        '''Compare the hash of a file in the bzip2 archive and the
        expected one
        '''
        __myobj = backupchecker.checkbackups.checkbzip2.CheckBzip2({'path':
            'tests/expected_hash/bar.bz2',
             'files_list':
                'tests/expected_hash/bzip2-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __hashes = __myobj.mismatched_hashes
        self.assertEqual(__hashes, [
            {'path': 'bar',
            'expectedhash': '768',
            'hash': '768d0a4cdfde46a468b6d9ba01a19a2a'}])

    def test_checktar_archive_equal_size(self):
        '''Check if the CheckTar class returns a dictionary with the
           archive itself file whose size should have been equal
           to the expected size.
        '''
        __missing_equality = []
        __missing_equality = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/arcsize/equaltararcsize-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'tests/file_size/essai.tar.bz2')
        
    def test_checktar_archive_missing_smaller_than(self):
        '''Check if the CheckTar class returns a dictionary with the
           archive itself whose size should have been smaller 
           than the expected size.
        '''
        __missing_smaller_than = []
        __missing_smaller_than = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/arcsize/biggerthantararcsize-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'tests/file_size/essai.tar.bz2')

    def test_checktar_archive_missing_bigger_than(self):
        '''Check if the CheckTar class returns a dictionary with the
           archive itself whose size should have been bigger 
           than the expected size.
        '''
        __missing_bigger_than = []
        __missing_bigger_than = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/arcsize/smallerthantararcsize-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'tests/file_size/essai.tar.bz2')

    def test_checkzip_archive_equal_size(self):
        '''Check if the CheckZip class returns a dictionary with the
           archive itself file whose size should have been equal
           to the expected size.
        '''
        __missing_equality = []
        __missing_equality = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/arcsize/equalziparcsize-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'tests/file_size/myzip.zip')
        
    def test_checkzip_archive_missing_smaller_than(self):
        '''Check if the CheckZip class returns a dictionary with the
           archive itself whose size should have been smaller 
           than the expected size.
        '''
        __missing_smaller_than = []
        __missing_smaller_than = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/arcsize/biggerthanziparcsize-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'tests/file_size/myzip.zip')

    def test_checkzip_archive_missing_bigger_than(self):
        '''Check if the CheckZip class returns a dictionary with the
           archive itself whose size should have been bigger 
           than the expected size.
        '''
        __missing_bigger_than = []
        __missing_bigger_than = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/arcsize/smallerthanziparcsize-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'tests/file_size/myzip.zip')

    def test_checktar_md5_hash_archive(self):
        '''Check the md5 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = backupchecker.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/md5hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': '47907de120577e6ba3b9dd8821374937',
            'hash': '47907de120577e6ba3b9dd8821374936'})

    def test_checktar_sha1_hash_archive(self):
        '''Check the sha1 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = backupchecker.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha1hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': '84db203e2902fa5ea51e6d46ea365c7bfc5524b9',
            'hash': '84db203e2902fa5ea51e6d46ea365c7bfc5524b8'})

    def test_checktar_sha224_hash_archive(self):
        '''Check the sha224 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = backupchecker.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha224hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': 'e25621dfdd2b2cfca451c735f4e676653e8628187e2b7ddc14402c1e',
            'hash': 'e25621dfdd2b2cfca451c735f4e676653e8628187e2b7ddc14402c1d'})

    def test_checktar_sha256_hash_archive(self):
        '''Check the sha256 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = backupchecker.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha256hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': '7090d29295216e95ab4a190d489aa405d141cac978567c227f17ee78eb3f5fd5',
            'hash': '7090d29295216e95ab4a190d489aa405d141cac978567c227f17ee78eb3f5fd4'})

    def test_checktar_sha384_hash_archive(self):
        '''Check the sha384 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = backupchecker.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha384hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': 'aa01a55142a04de52cebba3797ca25054e51c33a5fbfdc4dd0cc2f01f6252c6a62cb87f35405d9d8b07a506eefacfd11',
            'hash': 'aa01a55142a04de52cebba3797ca25054e51c33a5fbfdc4dd0cc2f01f6252c6a62cb87f35405d9d8b07a506eefacfd10'})

    def test_checktar_sha512_hash_archive(self):
        '''Check the sha512 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = backupchecker.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha512hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': 'd72eef1d9c42615f6b2a92848e8fa65ffd4276d91d9976fa8c644b41c15d91441ae42f897b30a2403795a876b14ae6ed8addca4a74f24839f6506a29e662e588',
            'hash': 'd72eef1d9c42615f6b2a92848e8fa65ffd4276d91d9976fa8c644b41c15d91441ae42f897b30a2403795a876b14ae6ed8addca4a74f24839f6506a29e662e587'})

    def test_checkzip_md5_hash_archive(self):
        '''Check the md5 hash of the zip archive itself using CheckTar class'''
        __mismatchedhashes = backupchecker.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/md5hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': 'e48e1ce2fbe0db616632ba8030ac2c9e',
            'hash': 'e48e1ce2fbe0db616632ba8030ac2c9f'})

    def test_checkzip_sha1_hash_archive(self):
        '''Check the sha1 hash of the zip archive itself using CheckTar class'''
        __mismatchedhashes = backupchecker.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha1hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '4cd5933d78603d8b4ba484ef8e45d2b6bc9fd5ce',
            'hash': '4cd5933d78603d8b4ba484ef8e45d2b6bc9fd5cf'})

    def test_checkzip_sha224_hash_archive(self):
        '''Check the sha224 hash of the zip archive itself using CheckTar class'''
        __mismatchedhashes = backupchecker.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha224hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '6e0838302f48cc7863a160f197a23492833b59862d89cabc46c2a1c4',
            'hash': '6e0838302f48cc7863a160f197a23492833b59862d89cabc46c2a1c3'})

    def test_checkzip_sha256_hash_archive(self):
        '''Check the sha256 hash of the zip archive itself using CheckZip class'''
        __mismatchedhashes = backupchecker.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha256hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '358bae9af3f9f510095b2e2a245a5e49ab27d7de862cd22f0dd4f212e25fb139',
            'hash': '358bae9af3f9f510095b2e2a245a5e49ab27d7de862cd22f0dd4f212e25fb138'})

    def test_checkzip_sha384_hash_archive(self):
        '''Check the sha384 hash of the zip archive itself using CheckZip class'''
        __mismatchedhashes = backupchecker.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha384hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '6a372e2867442826b64d1e3bca4b35e18d12d5df25e89decff214023d45f7f85d07ee79e6522f53961626e525ee29988',
            'hash': '6a372e2867442826b64d1e3bca4b35e18d12d5df25e89decff214023d45f7f85d07ee79e6522f53961626e525ee29989'})

    def test_checkzip_sha512_hash_archive(self):
        '''Check the sha512 hash of the zip archive itself using CheckZip class'''
        __mismatchedhashes = backupchecker.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha512hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': 'c177ca5b618ca613f27c44991eabb922d589691000fa602a0d2767ba84b317c653e6ed541f5922d201d2e65158eee4cfb7d87665bbe1d31c07f636bb25dac7b2',
            'hash': 'c177ca5b618ca613f27c44991eabb922d589691000fa602a0d2767ba84b317c653e6ed541f5922d201d2e65158eee4cfb7d87665bbe1d31c07f636bb25dac7b3'})


    def test_compare_tar_archive_uid_gid(self):
        '''Compare the uid and the gid of the tar archive itself
        and the expected one
        '''
        __uids = []
        __gids = []
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/expected_uid_gid/arc_uid_gid/uid-gid.tar.gz',
             'files_list':
                'tests/expected_uid_gid/arc_uid_gid/tar-uid-gid-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __uids = __myobj.mismatched_uids
        __gids = __myobj.mismatched_gids
        self.assertEqual((__uids[0],__gids[0]), (
        {'path':'tests/expected_uid_gid/arc_uid_gid/uid-gid.tar.gz','expecteduid':5,'uid':os.getuid()},
        {'path':'tests/expected_uid_gid/arc_uid_gid/uid-gid.tar.gz','expectedgid':6,'gid':os.getgid()}))

    def test_compare_zip_archive_uid_gid(self):
        '''Compare the uid and the gid of the zip archive itself
        and the expected one
        '''
        __uids = []
        __gids = []
        __myobj = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/expected_uid_gid/arc_uid_gid/uid-gid.zip',
             'files_list':
                'tests/expected_uid_gid/arc_uid_gid/zip-uid-gid-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __uids = __myobj.mismatched_uids
        __gids = __myobj.mismatched_gids
        self.assertEqual((__uids[0],__gids[0]), (
        {'path':'tests/expected_uid_gid/arc_uid_gid/uid-gid.zip','expecteduid':5,'uid':os.getuid()},
        {'path':'tests/expected_uid_gid/arc_uid_gid/uid-gid.zip','expectedgid':6,'gid':os.getgid()}))

###########################################################
#
# Testing the private method from checkarchive.CheckArchive
#
###########################################################

    def test_extract_archive_info(self):
        '''test the extract_archive_info private method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __fileinfo = __myobj._CheckArchive__extract_archive_info(__file)
        self.assertEqual(type(os.lstat(__file)), type(__fileinfo))

    def test_find_archive_size(self):
        '''test the find_archive_size private method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __filesize = __myobj._CheckArchive__find_archive_size(__file)
        self.assertEqual(os.lstat(__file).st_size, __filesize)

    def test_find_archive_mode(self):
        '''test the find_archive_mode private method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __filemode = __myobj._CheckArchive__find_archive_mode(__file)
        self.assertEqual(stat.S_IMODE(os.lstat(__file).st_mode), __filemode)

    def test_find_archive_uid_gid(self):
        '''test the find_archive_uid_gid private method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __arcuid, __arcgid = __myobj._CheckArchive__find_archive_uid_gid(__file)
        __fileinfo = os.lstat(__file)
        __fileuid, __filegid = __fileinfo.st_uid, __fileinfo.st_gid
        self.assertEqual((__arcuid, __arcgid), (__fileuid, __filegid))

    def test_check_uid(self):
        ''' test checkarchive.CheckArchive__check_uid'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __myobj._CheckArchive__check_uid('1000', {'path':'test', 'uid':'999'})
        self.assertEqual([{'path':'test', 'expecteduid':'999', 'uid':'1000'}], __myobj.mismatched_uids)

    def test_check_gid(self):
        ''' test checkarchive.CheckArchive__check_gid'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __myobj._CheckArchive__check_gid('1000', {'path':'test', 'gid':'999'})
        self.assertEqual([{'path':'test', 'expectedgid':'999', 'gid':'1000'}], __myobj.mismatched_gids)

#############################################################
#
# Testing the protected method from checkarchive.CheckArchive
#
#############################################################

    def test_compare_sizes(self):
        '''test the compare_sizes method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __mydict1 = {'equals': 12}
        __mydict2 = {'biggerthan': 3}
        __mydict3 = {'smallerthan': 7}
        __myobj._compare_sizes(13, 'mytar1.tar.gz', __mydict1 )
        __myobj._compare_sizes(1, 'mytar2.tar.gz', __mydict2 )
        __myobj._compare_sizes(15, 'mytar3.tar.gz', __mydict3 )
        self.assertEqual(__myobj.missing_equality, [{'expected': 12, 'path': 'mytar1.tar.gz', 'size': 13}])
        self.assertEqual(__myobj.missing_bigger_than, [{'expected': 3, 'path': 'mytar2.tar.gz', 'size': 1}])
        self.assertEqual(__myobj.missing_smaller_than, [{'expected': 7, 'path': 'mytar3.tar.gz', 'size': 15}])

    def test_normalize_path(self):
        '''test the normalize_path method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __res = __myobj._normalize_path('/test/')
        self.assertEqual(__res, '/test')

    def test_check_unexpected_files(self):
        '''test the check_unexpected_files method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __myobj._check_unexpected_files('test.tar.gz', 'unexpected weird ok')
        self.assertEqual(__myobj.unexpected_files, ['test.tar.gz'])

    def test_check_mode(self):
        '''test the check_mode method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __myobj._check_mode(777, {'path': 'test.tar.gz', 'mode':'644'})
        self.assertEqual(__myobj.mismatched_modes, [{'path': 'test.tar.gz', 'mode':'1411', 'expectedmode':'644'}])

    def test_check_type(self):
        '''test the check_type method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __myobj._check_type('s', {'path': 'test.tar.gz', 'type':'f'})
        self.assertEqual(__myobj.mismatched_types, [{'path': 'test.tar.gz', 'type':'s', 'expectedtype':'f'}])

    def test_check_mtime(self):
        '''test the check_mtime method from CheckArchive'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __myobj._check_mtime(1383912787.0, {'path': 'test.tar.gz', 'mtime': 1383912786.0})
        self.assertEqual(__myobj.mismatched_mtimes, [{'path': 'test.tar.gz', 'mtime': 1383912787.0, 'expectedmtime': 1383912786.0}])

##############################################################
#
# Testing the private/protected methods from checkzip.CheckZip 
#
##############################################################

    def test_zip_extract_stored_file(self):
        '''test the _extract_stored_file protected method from checkzip.CheckZip'''
        __myobj = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/checkzip_private_methods/myzip.zip',
             'files_list':
                'tests/checkzip_private_methods/myzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkzip_private_methods/myzip.zip'
        self._zip = zipfile.ZipFile(__file,'r')
        __result = __myobj._extract_stored_file('file-missing-in-zip/foo')
        self.assertEqual(type(__result), type(self._zip.open('file-missing-in-zip/foo')))

    def test_zip_extract_uid_gid(self):
        '''test the __extract_uid_gid private method from checkzip.CheckZip'''
        __myobj = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/checkzip_private_methods/myzip.zip',
             'files_list':
                'tests/checkzip_private_methods/myzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkzip_private_methods/myzip.zip'
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._CheckZip__extract_uid_gid(__myinfo[-1])
        self.assertEqual((1000,1000), __result)

    def test_zip_translate_type_file(self):
        '''test the __translate_type private method from checkzip.CheckZip - expecting file'''
        __myobj = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/checkzip_private_methods/myzip.zip',
             'files_list':
                'tests/checkzip_private_methods/myzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkzip_private_methods/myzip.zip'
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._CheckZip__translate_type(__myinfo[-1].external_attr >> 16)
        self.assertEqual('f', __result)

    def test_zip_translate_type_directory(self):
        '''test the __translate_type private method from checkzip.CheckZip - expecting directory'''
        __myobj = backupchecker.checkbackups.checkzip.CheckZip({'path':
            'tests/checkzip_private_methods/myzip.zip',
             'files_list':
                'tests/checkzip_private_methods/myzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkzip_private_methods/myzip.zip'
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._CheckZip__translate_type(__myinfo[0].external_attr >> 16)
        self.assertEqual('d', __result)

##############################################################
#
# Testing the private/protected methods from checktar.CheckTar 
#
##############################################################

    def test_tar_extract_stored_file(self):
        '''test the _extract_stored_file protected method from checktar.CheckTar'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checktar_private_methods/mytargz/mytargz.tar.gz',
             'files_list':
                'tests/checktar_private_methods/mytargz/mytargz-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checktar_private_methods/mytargz/mytargz.tar.gz'
        self._tar = tarfile.open(__file)
        __result = __myobj._extract_stored_file('mytargz/hello')
        self.assertEqual(type(__result), type(self._tar.extractfile('mytargz/hello')))

    def test_tar_translate_type_file(self):
        '''test the __translate_type private method from checktar.CheckTar - expecting file'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checktar_private_methods/mytargz/mytargz.tar.gz',
             'files_list':
                'tests/checktar_private_methods/mytargz/mytargz-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checktar_private_methods/mytargz/mytargz.tar.gz'
        self._tar = tarfile.open(__file)
        __result = __myobj._CheckTar__translate_type(self._tar.getmembers()[2].type)
        self.assertEqual('f', __result)

    def test_tar_translate_type_directory(self):
        '''test the __translate_type private method from checktar.CheckTar - expecting directory'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checktar_private_methods/mytargz/mytargz.tar.gz',
             'files_list':
                'tests/checktar_private_methods/mytargz/mytargz-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checktar_private_methods/mytargz/mytargz.tar.gz'
        self._tar = tarfile.open(__file)
        __result = __myobj._CheckTar__translate_type(self._tar.getmembers()[0].type)
        self.assertEqual('d', __result)

    def test_tar_translate_type_symbolic_link(self):
        '''test the __translate_type private method from checktar.CheckTar - expecting symbolic link'''
        __myobj = backupchecker.checkbackups.checktar.CheckTar({'path':
            'tests/checktar_private_methods/mytargz/mytargz.tar.gz',
             'files_list':
                'tests/checktar_private_methods/mytargz/mytargz-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checktar_private_methods/mytargz/mytargz.tar.gz'
        self._tar = tarfile.open(__file)
        __result = __myobj._CheckTar__translate_type(self._tar.getmembers()[1].type)
        self.assertEqual('s', __result)

################################################################
#
# Testing the private/protected methods from checktree.CheckTree
#
################################################################

    def test_tree_extract_stored_file(self):
        '''test the _extract_stored_file protected method from checktree.CheckTree'''
        __myobj = backupchecker.checkbackups.checktree.CheckTree({'path':
            'tests/checktree_private_methods/mytree',
             'files_list':
                'tests/checktree_private_methods/mytree-list',
             'type': 'tree', 'delimiter': ''}, Options())
        __file = 'tests/checktree_private_methods/mytree'
        __result = __myobj._extract_stored_file('hello')
        with open(os.path.join(__file, 'hello'), 'rb') as self.__desc:
            self.assertEqual(type(__result), type(self.__desc))
            __result.close()

    def test_tree_translate_type_file(self):
        '''test the __translate_type private method from checktree.CheckTree - expecting file'''
        __myobj = backupchecker.checkbackups.checktree.CheckTree({'path':
            'tests/checktree_private_methods/mytree',
             'files_list':
                'tests/checktree_private_methods/mytree-list',
             'type': 'tree', 'delimiter': ''}, Options())
        __file = 'tests/checktree_private_methods/mytree/hello'
        __result = __myobj._CheckTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('f', __result)

    def test_tree_translate_type_directory(self):
        '''test the __translate_type private method from checktree.CheckTree - expecting directory'''
        __myobj = backupchecker.checkbackups.checktree.CheckTree({'path':
            'tests/checktree_private_methods/mytree',
             'files_list':
                'tests/checktree_private_methods/mytree-list',
             'type': 'tree', 'delimiter': ''}, Options())
        __file = 'tests/checktree_private_methods/mytree'
        __result = __myobj._CheckTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('d', __result)

    def test_tree_translate_type_symbolic_link(self):
        '''test the __translate_type private method from checktree.CheckTree - expecting symbolic link'''
        __myobj = backupchecker.checkbackups.checktree.CheckTree({'path':
            'tests/checktree_private_methods/mytree',
             'files_list':
                'tests/checktree_private_methods/mytree-list',
             'type': 'tree', 'delimiter': ''}, Options())
        __file = 'tests/checktree_private_methods/mytree/riri'
        __result = __myobj._CheckTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('s', __result)

################################################################
#
# Testing the private/protected methods from checkgzip.CheckGzip
#
################################################################

    def test_gzip_extract_stored_file(self):
        '''test the _extract_stored_file protected method from checkgzip.CheckGzip'''
        __myobj = backupchecker.checkbackups.checkgzip.CheckGzip({'path':
            'tests/checkgzip_private_methods/mygzip.gz',
             'files_list':
                'tests/checkgzip_private_methods/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkgzip_private_methods/mygzip.gz'
        __result = __myobj._extract_stored_file('mygzip')
        with gzip.open(__file, 'rb') as self.__desc:
            self.assertEqual(type(__result), type(self.__desc))
            __result.close()

    def test_extract_size_from_gzip_archive(self):
        '''test the extraction of a gzip uncompressed file in the gzip archive'''
        __arcpath = 'tests/checkgzip_private_methods/mygzip.gz'
        __myobj = backupchecker.checkbackups.checkgzip.CheckGzip({'path':
            __arcpath,
             'files_list':
                'tests/checkgzip_private_methods/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        with open(__arcpath, 'rb') as __myf:
            self.assertEqual(23, __myobj._CheckGzip__extract_size(__myf))

    def test_extract_initial_filename_from_gzip_archive(self):
        '''test the extraction of the initial name of an uncompressed file'''
        __arcpath = 'tests/checkgzip_private_methods/mygzip.gz'
        __myobj = backupchecker.checkbackups.checkgzip.CheckGzip({'path':
            __arcpath,
             'files_list':
                'tests/checkgzip_private_methods/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        with open(__arcpath, 'rb') as __myf:
            self.assertEqual('mygzip', __myobj._CheckGzip__extract_initial_filename(__myf, 'mygzip'))

##################################################################
#
# Testing the private/protected methods from checkbzip2.CheckBzip2
#
##################################################################

    def test_bzip2_extract_stored_file(self):
        '''test the _extract_stored_file protected method from checkbzip2.CheckBzip2'''
        __myobj = backupchecker.checkbackups.checkbzip2.CheckBzip2({'path':
            'tests/checkbzip2_private_methods/mybz2.bz2',
             'files_list':
                'tests/checkbzip2_private_methods/mybzip2-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkbzip2_private_methods/mybz2.bz2'
        __result = __myobj._extract_stored_file('mygzip')
        with bz2.BZ2File(__file, 'r') as self.__desc:
            self.assertEqual(type(__result), type(self.__desc))
            __result.close()

######################################################################################
#
# Testing the private/protected methods from generatelistforbzip2.GenerateListForBzip2
#
######################################################################################

    def test__listconfinfo(self):
        '''test the GenerateListForBzip2 class'''
        __myobj = backupchecker.generatelist.generatelistforbzip2.GenerateListForBzip2({
            'arcpath': 'tests/checkbzip2_private_methods/mybz2.bz2', 'delimiter': '|', 'hashtype': '', 'parsingexceptions' : '', 'getallhashes': True, 'genfull': True, 'confoutput':'','listoutput':'','fulloutput':''})
        self.assertEqual(__myobj._GenerateListForBzip2__lci, {'arclistpath': 'tests/checkbzip2_private_methods/mybz2.list',
            'listoffiles': ['[files]\n', 'mybz2| type|f md5|f5488b7ce878d89b59ef2752f260354f\n']})
        self.assertEqual(__myobj._GenerateListForBzip2__ci, {'arcconfpath': 'tests/checkbzip2_private_methods/mybz2.conf',
            'arclistpath': 'tests/checkbzip2_private_methods/mybz2.list',
            'arcname': 'mybz2',
            'arcpath': 'tests/checkbzip2_private_methods/mybz2.bz2',
            'arctype': 'archive',
            'sha512': 'b45fa678a2208bfbf457f602b2d3de0c83e82ad9ba042b029b8d37f23bfe2774d1cd25576da880d20bb7f6ffcfc2ecb4bcc80112e880415de82fe63d81f81cb7'})

###############################################################################################
#
# Testing the private/protected methods from generatelist.generatelist.GenerateList 
#
###############################################################################################

    def test_generatelist_generate_list(self):
        '''test the _generate_list protected method from GenerateList'''
        __file = 'tests/generatelist_private_methods/mytar.list'
        __myobj = backupchecker.generatelist.generatelist.GenerateList()
        __content = ['[files]\n', 'foo:\n']
        __myobj._generate_list({'arclistpath': __file, 'listoffiles': __content})
        with open(__file, 'r') as __f:
            self.assertEqual(__f.readlines(), __content)

###############################################################################################
#
# Testing the private/protected methods from generatelist.generatelistfortar.GenerateListForTar 
#
###############################################################################################

    def test_listfortar_translate_type_file(self):
        '''test the __translate_type private method from GenerateListForTar - expecting file'''
        __file = 'tests/generatelistfortar_private_methods/mytar.tar.gz'
        __myobj = backupchecker.generatelist.generatelistfortar.GenerateListForTar({'arcpath':__file, 'delimiter':DEFAULTDELIMITER,  'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':'', 'isastream':False})
        self.__tar = tarfile.open(__file)
        __result = __myobj._GenerateListForTar__translate_type(self.__tar.getmembers()[3].type)
        self.assertEqual('f', __result)

    def test_listfortar_translate_type_directory(self):
        '''test the __translate_type private method from GenerateListForTar - expecting directory'''
        __file = 'tests/generatelistfortar_private_methods/mytar.tar.gz'
        __myobj = backupchecker.generatelist.generatelistfortar.GenerateListForTar({'arcpath':__file, 'delimiter':DEFAULTDELIMITER,  'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':'', 'isastream':False})
        self.__tar = tarfile.open(__file)
        __result = __myobj._GenerateListForTar__translate_type(self.__tar.getmembers()[1].type)
        self.assertEqual('d', __result)

    def test_listfortar_translate_type_symbolic_link(self):
        '''test the __translate_type private method from GenerateListForTar - expecting symbolic link'''
        __file = 'tests/generatelistfortar_private_methods/mytar.tar.gz'
        __myobj = backupchecker.generatelist.generatelistfortar.GenerateListForTar({'arcpath':__file, 'delimiter':DEFAULTDELIMITER,  'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':'', 'isastream':False})
        self.__tar = tarfile.open(__file)
        __result = __myobj._GenerateListForTar__translate_type(self.__tar.getmembers()[2].type)
        self.assertEqual('s', __result)

###############################################################################################
#
# Testing the private/protected methods from generatelist.generatelistforzip.GenerateListForZip 
#
###############################################################################################

    def test_listforzip_translate_type_file(self):
        '''test the __translate_type private method from GenerateListForZip - expecting file'''
        __file = 'tests/generatelistforzip_private_methods/myzip.zip'
        __myobj = backupchecker.generatelist.generatelistforzip.GenerateListForZip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':''})
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._GenerateListForZip__translate_type(__myinfo[-1].external_attr >> 16)
        self.assertEqual('f', __result)

    def test_listforzip_translate_type_directory(self):
        '''test the __translate_type private method from GenerateListForZip - expecting directory'''
        __file = 'tests/generatelistforzip_private_methods/myzip.zip'
        __myobj = backupchecker.generatelist.generatelistforzip.GenerateListForZip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':''})
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._GenerateListForZip__translate_type(__myinfo[0].external_attr >> 16)
        self.assertEqual('d', __result)

    def test_listforzip_extract_uid_gid(self):
        '''test the __extract_uid_gid private method from GenerateListForZip'''
        __file = 'tests/generatelistforzip_private_methods/myzip.zip'
        __myobj = backupchecker.generatelist.generatelistforzip.GenerateListForZip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':''})
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._GenerateListForZip__extract_uid_gid(__myinfo[-1])
        self.assertEqual((1000,1000), __result)

#################################################################################################
#
# Testing the private/protected methods from generatelist.generatelistfortree.GenerateListForTree 
#
#################################################################################################

    def test_listfortree_translate_type_file(self):
        '''test the __translate_type private method from GenerateListForTree - expecting file'''
        __dir = 'tests/generatelistfortree_private_methods/mydir'
        __file = os.path.join(__dir, 'foo')
        __myobj = backupchecker.generatelist.generatelistfortree.GenerateListForTree({'arcpath':__file, 'delimiter':DEFAULTDELIMITER,  'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':''})
        __myobj._GenerateListForTree__fileinfo = os.lstat(__file)
        __result = __myobj._GenerateListForTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('f', __result)

    def test_listfortree_translate_type_directory(self):
        '''test the __translate_type private method from GenerateListForTree - expecting directory'''
        __dir = 'tests/generatelistfortree_private_methods/mydir'
        __file = os.path.join(__dir, 'bar')
        __myobj = backupchecker.generatelist.generatelistfortree.GenerateListForTree({'arcpath':__file, 'delimiter':DEFAULTDELIMITER,  'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':''})
        __result = __myobj._GenerateListForTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('d', __result)

    def test_listfortree_translate_type_symbolic_link(self):
        '''test the __translate_type private method from GenerateListForTree - expecting symbolic link'''
        __dir = 'tests/generatelistfortree_private_methods/mydir'
        __file = os.path.join(__dir, 'oof')
        __myobj = backupchecker.generatelist.generatelistfortree.GenerateListForTree({'arcpath':__file, 'delimiter':DEFAULTDELIMITER,  'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':''})
        __result = __myobj._GenerateListForTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('s', __result)

#################################################################################################
#
# Testing the private/protected methods from generatelist.generatelistfortree.GenerateListForTree 
#
#################################################################################################

    def test_listforgzip_extract_size_from_gzip_archive(self):
        '''test the extraction of a gzip uncompressed file in the gzip archive'''
        __file = 'tests/generatelistforgzip_private_methods/mygzip.gz'
        __myobj = backupchecker.generatelist.generatelistforgzip.GenerateListForGzip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER,  'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':''})
        with open(__file, 'rb') as __myf:
            self.assertEqual(15, __myobj._GenerateListForGzip__extract_size(__myf))

    def test_listforgzip_extract_initial_filename_from_gzip_archive(self):
        __file = 'tests/generatelistforgzip_private_methods/mygzip.gz'
        __myobj = backupchecker.generatelist.generatelistforgzip.GenerateListForGzip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER,  'hashtype': '', 'parsingexceptions': '', 'getallhashes': False, 'genfull':False, 'confoutput':'','listoutput':'','fulloutput':''})
        with open(__file, 'rb') as __myf:
            self.assertEqual('mygzip', __myobj._GenerateListForGzip__extract_initial_filename(__myf, 'mygzip'))

##############################################################
#
# Testing the private/protected methods from cliparse.CliParse
#
##############################################################

    def test_cliparse_cliparse(self):
        '''Test the cliparse.CliParse class'''
        __archivepath = '/tmp/archive.conf'
        __logpath = '/tmp/a.out'
        with open(__archivepath, 'w') as __desc:
            __desc.write('')
        sys.argv.append('-c')
        sys.argv.append(__archivepath)
        sys.argv.append('-l')
        sys.argv.append(__logpath)
        __myobj = backupchecker.cliparse.CliParse()
        self.assertEqual(vars(__myobj.options), {'archives': [],
            'confpath': __archivepath,
            'delimiter': '|',
            'hashtype': '',
            'parsingexceptions': '',
            'getallhashes': False,
            'genfull': False,
            'genlist': False,
            'logfile': __logpath,
            'fulloutput':'',
            'confoutput':'',
            'listoutput':''})
        os.remove(__archivepath)

#######################################################################################
#
# Testing the consistent given version of the software both in setup.py and cliparse.py
#
#######################################################################################

    def test_version_consistency_in_setup_py_and_cliparse_py(self):
        '''test the consistency of the version of the software
           in both setup.py and cliparse.py
        '''
        with open('setup.py') as __setuppy:
            __setuppycode = __setuppy.readlines()
        with open('backupchecker/cliparse.py') as __cliparsepy:
            __cliparsepycode = __cliparsepy.readlines()
        for line in __setuppycode:
            if 'version = ' in line:
                setuppyversion = line.split("'")[1]
                break
        for line in __cliparsepycode:
            if 'version=' in line:
                cliparsepyversion = line.split('s ')[1].split("'")[0]
                break
        self.assertEqual(setuppyversion, cliparsepyversion)

#######################################################################################
#
# Testing the backupchecker/archiveinfomsg.py
#
#######################################################################################

    def test_archiveinfomsg_main(self):
        '''test the archivemsginfo.ArchiveMsgInfo__main method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = ['testarchiveinfomsgmain1']
        __mydict.unexpected_files = []
        __mydict.missing_equality = []
        __mydict.missing_smaller_than = []
        __mydict.missing_bigger_than = []
        __mydict.missing_bigger_than = []
        __mydict.mismatched_uids = []
        __mydict.mismatched_gids = []
        __mydict.mismatched_modes = []
        __mydict.mismatched_types = []
        __mydict.mismatched_hashes = []
        __mydict.mismatched_targets = []
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testarchiveinfomsgmain.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__main(__mydict, {'path': 'testarchiveinfomsgmain.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        with open(_logfile) as _res:
            self.assertIn('WARNING:root:1 file missing in testarchiveinfomsgmain.tar.gz: \nWARNING:root:testarchiveinfomsgmain1\n', _res.read())

    def test_archiveinfomsg_missing_files(self):
        '''test the __missing_files method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = []
        __mydict.unexpected_files = []
        __mydict.missing_equality = []
        __mydict.missing_smaller_than = []
        __mydict.missing_bigger_than = []
        __mydict.missing_bigger_than = []
        __mydict.mismatched_uids = []
        __mydict.mismatched_gids = []
        __mydict.mismatched_modes = []
        __mydict.mismatched_types = []
        __mydict.mismatched_hashes = []
        __mydict.mismatched_targets = []
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testmissingfiles.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__missing_files(['titi'], 'testmissingfiles.tar.gz')
        with open(_logfile) as _res:
            self.assertIn('WARNING:root:1 file missing in testmissingfiles.tar.gz: \nWARNING:root:titi\n', _res.read())

    def test_archiveinfomsg_unexpected_files(self):
        '''test the archiveinfomsg.ArchiveInfoMsg__unexpected_files method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = []
        __mydict.unexpected_files = []
        __mydict.missing_equality = []
        __mydict.missing_smaller_than = []
        __mydict.missing_bigger_than = []
        __mydict.missing_bigger_than = []
        __mydict.mismatched_uids = []
        __mydict.mismatched_gids = []
        __mydict.mismatched_modes = []
        __mydict.mismatched_types = []
        __mydict.mismatched_hashes = []
        __mydict.mismatched_targets = []
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testunexpectedfiles.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__unexpected_files(['titi'], 'testunexpectedfiles.tar.gz')
        with open(_logfile) as _res:
            self.assertIn('WARNING:root:1 unexpected file checking testunexpectedfiles.tar.gz: \nWARNING:root:titi\n', _res.read())

    def test_archiveinfomsg_classify_differences(self):
        '''test the archiveinfomsg.ArchiveInfoMsg__classify_differences method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = []
        __mydict.unexpected_files = []
        __mydict.missing_equality = [{'path':'classifydifferences1', 'size':'12','expected':'3'}]
        __mydict.missing_smaller_than = [{'path':'classifydifferences2', 'size':'12','expected':'3'}]
        __mydict.missing_bigger_than = [{'path':'classifydifferences3', 'size':'12','expected':'3'}]
        __mydict.mismatched_uids = []
        __mydict.mismatched_gids = []
        __mydict.mismatched_modes = []
        __mydict.mismatched_types = []
        __mydict.mismatched_hashes = []
        __mydict.mismatched_targets = []
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testclassifydifferences.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__classify_differences(__mydict, 'testclassifydifferences.tar.gz')
        with open(_logfile) as _res:
            __testresult = _res.read()
            self.assertIn('WARNING:root:classifydifferences1 size is 12. Should have been 3.', __testresult)
            self.assertIn('WARNING:root:classifydifferences2 size is 12. Should have been smaller than 3.', __testresult)
            self.assertIn('WARNING:root:classifydifferences3 size is 12. Should have been bigger than 3.', __testresult)

    def test_archiveinfomsg_log_differences(self):
        '''test the archiveinfomsg.ArchiveInfoMsg__log_differences method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = []
        __mydict.unexpected_files = []
        __mydict.missing_equality = [{'path':'classifydifferences4', 'size':'12','expected':'3'}]
        __mydict.missing_smaller_than = []
        __mydict.missing_bigger_than = []
        __mydict.mismatched_uids = []
        __mydict.mismatched_gids = []
        __mydict.mismatched_modes = []
        __mydict.mismatched_types = []
        __mydict.mismatched_hashes = []
        __mydict.mismatched_targets = []
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testlogdifferences.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__log_differences(__mydict.missing_equality, 'testlogdifferences.tar.gz', '{} {} with unexpected size while checking {}: ')
        with open(_logfile) as _res:
            __testresult = _res.read()
            self.assertIn('WARNING:root:classifydifferences4 size is 12. Should have been 3.', __testresult)

    def test_archiveinfomsg_uid_gid_mismatches(self):
        '''test the archiveinfomsg.ArchiveInfoMsg__uid_gid_mismatches method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = []
        __mydict.unexpected_files = []
        __mydict.missing_equality = []
        __mydict.missing_smaller_than = []
        __mydict.missing_bigger_than = []
        __mydict.mismatched_uids = [{'path':'classifydifferences5', 'expecteduid':'1010','uid':'1000'}]
        __mydict.mismatched_gids = [{'path':'classifydifferences6', 'expectedgid':'1010','gid':'1000'}]
        __mydict.mismatched_modes = []
        __mydict.mismatched_types = []
        __mydict.mismatched_hashes = []
        __mydict.mismatched_targets = []
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testuidgidmismatches.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__uid_gid_mismatches(__mydict, 'testuidgidmismatches.tar.gz')
        with open(_logfile) as _res:
            __testresult = _res.read()
            self.assertIn('WARNING:root:classifydifferences5 uid is 1000. Should have been 1010.', __testresult)
            self.assertIn('WARNING:root:classifydifferences6 gid is 1000. Should have been 1010.', __testresult)

    def test_archiveinfomsg_mode_mismatches(self):
        '''test the archiveinfomsg.ArchiveInfoMsg__mode_mismatches method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = []
        __mydict.unexpected_files = []
        __mydict.missing_equality = []
        __mydict.missing_smaller_than = []
        __mydict.missing_bigger_than = []
        __mydict.mismatched_uids = []
        __mydict.mismatched_gids = []
        __mydict.mismatched_modes = [{'path':'classifydifferences7', 'expectedmode':'644','mode':'777'}]
        __mydict.mismatched_types = []
        __mydict.mismatched_hashes = []
        __mydict.mismatched_targets = []
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testmodemismatches.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__mode_mismatches(__mydict, 'testmodemismatches.tar.gz')
        with open(_logfile) as _res:
            __testresult = _res.read()
            self.assertIn('WARNING:root:classifydifferences7 mode is 777. Should have been 644.', __testresult)

    def test_archiveinfomsg_target_mismatches(self):
        '''test the archiveinfomsg.ArchiveInfoMsg__target_mismatches method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = []
        __mydict.unexpected_files = []
        __mydict.missing_equality = []
        __mydict.missing_smaller_than = []
        __mydict.missing_bigger_than = []
        __mydict.mismatched_uids = []
        __mydict.mismatched_gids = []
        __mydict.mismatched_modes = []
        __mydict.mismatched_types = []
        __mydict.mismatched_hashes = []
        __mydict.mismatched_targets = [{'path':'classifydifferences8', 'expectedtarget':'../target1','target':'../target2'}]
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testtargetmismatches.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__target_mismatches(__mydict, 'testtargetmismatches.tar.gz')
        with open(_logfile) as _res:
            __testresult = _res.read()
            self.assertIn('WARNING:root:classifydifferences8 target is ../target2. Should have been ../target1.', __testresult)

    def test_archiveinfomsg_type_mismatches(self):
        '''test the archiveinfomsg.ArchiveInfoMsg__type_mismatches method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = []
        __mydict.unexpected_files = []
        __mydict.missing_equality = []
        __mydict.missing_smaller_than = []
        __mydict.missing_bigger_than = []
        __mydict.mismatched_uids = []
        __mydict.mismatched_gids = []
        __mydict.mismatched_modes = []
        __mydict.mismatched_types = [{'path':'classifydifferences9', 'expectedtype':'s','type':'f'}]
        __mydict.mismatched_hashes = []
        __mydict.mismatched_targets = []
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testtypemismatches.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__target_mismatches(__mydict, 'testtypemismatches.tar.gz')
        with open(_logfile) as _res:
            __testresult = _res.read()
            self.assertIn('WARNING:root:classifydifferences9 is a regular file. Should have been a symbolic link.', __testresult)

    def test_archiveinfomsg_hash_mismatches(self):
        '''test the archiveinfomsg.ArchiveInfoMsg__hash_mismatches method'''
        _logfile = TESTLOG
        backupchecker.applogger.AppLogger(TESTLOG)
        __mydict = MyDict()
        __mydict.missing_files = []
        __mydict.unexpected_files = []
        __mydict.missing_equality = []
        __mydict.missing_smaller_than = []
        __mydict.missing_bigger_than = []
        __mydict.mismatched_uids = []
        __mydict.mismatched_gids = []
        __mydict.mismatched_modes = []
        __mydict.mismatched_types = []
        __mydict.mismatched_hashes = [{'path':'classifydifferences10', 'expectedhash':'azeraezr','hash':'qdslfmjaze'}]
        __mydict.mismatched_targets = []
        __mydict.mismatched_mtimes = []
        __mydict.mismatched_unames = []
        __mydict.mismatched_gnames = []
        __myobj = backupchecker.archiveinfomsg.ArchiveInfoMsg(__mydict, {'path': 'testhashmismatches.tar.gz', 'sha512': None, 'files_list': '', 'type': 'archive', 'delimiter': None})
        __myobj._ArchiveInfoMsg__hash_mismatches(__mydict, 'testhashmismatches.tar.gz')
        with open(_logfile) as _res:
            __testresult = _res.read()
            self.assertIn('WARNING:root:classifydifferences10 hash is qdslfmjaze. Should have been azeraezr.', __testresult)

#######################################################################################
#
# Testing the backupchecker.listtype.ListType
#
#######################################################################################

    def test_listtype_tar(self):
        '''test the listtype class with a tar archive'''
        #__mydict = backupchecker.listtype.ListType({'arcpath': 'test.tar.gz', 'delimiter': None, 'genfull': True})
        __mydict = MyDict()
        __mydict.archives = ['tests/listtype/mytargz.tar.gz']
        __mydict.delimiter = None
        __mydict.hashtype = ''
        __mydict.genfull = True
        __mydict.getallhashes = True
        __mydict.fulloutput = ''
        __mydict.confoutput = ''
        __mydict.listoutput = ''
        __mydict.isastream = False
        __mydict = backupchecker.listtype.ListType(__mydict)
        self.assertEqual(str(type(__mydict._ListType__bck)), "<class 'backupchecker.generatelist.generatelistfortar.GenerateListForTar'>")

    def test_listtype_tree(self):
        '''test the listtype class with a tree archive'''
        __mydict = MyDict()
        __mydict.archives = ['tests/listtype/mytree']
        __mydict.delimiter = None
        __mydict.hashtype = ''
        __mydict.genfull = True
        __mydict.getallhashes = True
        __mydict.fulloutput = ''
        __mydict.confoutput = ''
        __mydict.listoutput = ''
        __mydict.isastream = False
        __mydict = backupchecker.listtype.ListType(__mydict)
        self.assertEqual(str(type(__mydict._ListType__bck)), "<class 'backupchecker.generatelist.generatelistfortree.GenerateListForTree'>")

    def test_listtype_zip(self):
        '''test the listtype class with a zip archive'''
        __mydict = MyDict()
        __mydict.archives = ['tests/listtype/myzip.zip']
        __mydict.delimiter = None
        __mydict.hashtype = ''
        __mydict.genfull = True
        __mydict.getallhashes = True
        __mydict.fulloutput = ''
        __mydict.confoutput = ''
        __mydict.listoutput = ''
        __mydict.isastream = False
        __mydict = backupchecker.listtype.ListType(__mydict)
        self.assertEqual(str(type(__mydict._ListType__bck)), "<class 'backupchecker.generatelist.generatelistforzip.GenerateListForZip'>")

    def test_listtype_gz(self):
        '''test the listtype class with a gzip archive'''
        __mydict = MyDict()
        __mydict.archives = ['tests/listtype/mygzip.gz']
        __mydict.delimiter = None
        __mydict.hashtype = ''
        __mydict.genfull = True
        __mydict.getallhashes = True
        __mydict.fulloutput = ''
        __mydict.confoutput = ''
        __mydict.listoutput = ''
        __mydict.isastream = False
        __mydict = backupchecker.listtype.ListType(__mydict)
        self.assertEqual(str(type(__mydict._ListType__bck)), "<class 'backupchecker.generatelist.generatelistforgzip.GenerateListForGzip'>")

    def test_listtype_bz2(self):
        '''test the listtype class with a bzip2 archive'''
        __mydict = MyDict()
        __mydict.archives = ['tests/listtype/mybz2.bz2']
        __mydict.delimiter = None
        __mydict.hashtype = ''
        __mydict.genfull = True
        __mydict.getallhashes = True
        __mydict.fulloutput = ''
        __mydict.confoutput = ''
        __mydict.listoutput = ''
        __mydict.isastream = False
        __mydict = backupchecker.listtype.ListType(__mydict)
        self.assertEqual(str(type(__mydict._ListType__bck)), "<class 'backupchecker.generatelist.generatelistforbzip2.GenerateListForBzip2'>")

    def test_listtype_xz(self):
        '''test the listtype class with a lzma archive'''
        __mydict = MyDict()
        __mydict.archives = ['tests/listtype/mylzma.xz']
        __mydict.delimiter = None
        __mydict.hashtype = ''
        __mydict.genfull = True
        __mydict.getallhashes = True
        __mydict.fulloutput = ''
        __mydict.confoutput = ''
        __mydict.listoutput = ''
        __mydict.isastream = False
        __mydict = backupchecker.listtype.ListType(__mydict)
        self.assertEqual(str(type(__mydict._ListType__bck)), "<class 'backupchecker.generatelist.generatelistforlzma.GenerateListForLzma'>")

################################################################
#
# End of the unit tests
#
################################################################
    @classmethod
    def tearDownClass(TestApp):
        '''clean after the tests'''
        _logfile = TESTLOG
        os.remove(_logfile)

if __name__ == '__main__':
    unittest.main()
