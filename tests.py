#!/usr/bin/python3.3
# -*- coding: utf-8 -*-
# Copyright © 2013 Carl Chenet <chaica@ohmytux.com>
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

import brebis.applogger
import brebis.checkbackups.checkarchive
import brebis.checkbackups.checkbackups
import brebis.checkbackups.checkbzip2
import brebis.checkbackups.checkgzip
import brebis.checkhashes
import brebis.checkbackups.checktar
import brebis.checkbackups.checktree
import brebis.checkbackups.checkzip
import brebis.cliparse
import brebis.configurations
from brebis.expectedvalues import ExpectedValues
import brebis.generatelist.generatelistfortar
import brebis.main

# !! logging module uses a single logger for the whole file
TESTLOG = 'tests/testlog'
DEFAULTDELIMITER = '|'

# mock the object produced by argparse, useful for lots of tests below
class Options:
    '''Mock the object produced by argparse, useful for lots of unittests'''
    def __init__(self):
        self.delimiter = DEFAULTDELIMITER

class TestApp(unittest.TestCase):

    def test_applogger(self):
        '''Test the AppLoggerclass'''
        brebis.applogger.AppLogger(TESTLOG)
        self.assertEqual(True, str(logging.getLogger('applogger')).startswith('<logging.Logger object at'))
        
    def test_checkbackup(self):
        '''Test the CheckBackup class'''
        _logfile = TESTLOG
        brebis.applogger.AppLogger(_logfile)
        brebis.checkbackups.checkbackups.CheckBackups({'essai': {'path': 'tests/tar_gz_archive_content/essai.tar.gz', 'files_list': 'tests/tar_gz_archive_content/essai-list', 'type': 'archive','delimiter':''}, 'essai2': {'path': 'tests/tar_bz2_archive_content/titi.tar.bz2', 'files_list': 'tests/tar_bz2_archive_content/essai2-list', 'type': 'archive','delimiter':''}}, Options())
        with open(_logfile) as _res:
            self.assertEqual(_res.read(), 'WARNING:root:1 file missing in tests/tar_gz_archive_content/essai.tar.gz: \nWARNING:root:essai/dir/titi\n')
        os.remove(_logfile)

    def test_checktar_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        _missingfiles = []
        _missingfiles = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/tar_gz_archive_content/essai.tar.gz',
             'files_list':
                'tests/tar_gz_archive_content/essai-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_files
        self.assertEqual(_missingfiles, ['essai/dir/titi'])

    def test_checktar_missing_equality(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'essai/dir/toto')

    def test_checktar_missing_bigger_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'essai/titi')

    def test_checktar_missing_smaller_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'essai/dir/toutou')

    def test_checktree_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        __missing_files = []
        __missing_files = brebis.checkbackups.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree', 'delimiter': ''}, Options()).missing_files
        self.assertEqual(__missing_files, ['bar/toto'])

    def test_checktree_missing_equality(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality= []
        __missing_equality = brebis.checkbackups.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'foo1')

    def test_checktree_missing_bigger_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = brebis.checkbackups.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'foo2')

    def test_checktree_missing_smaller_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = brebis.checkbackups.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'bar/foo3')

    def test_checkgzip_missing_files(self):
        '''Check if the CheckGzip class returns a missing file'''
        _missing_files = []
        _missing_files = brebis.checkbackups.checkgzip.CheckGzip({'path':
            'tests/gzip/mygzip.gz',
             'files_list':
                'tests/gzip/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_files
        self.assertEqual(_missing_files, ['foo'])

    def test_checkgzip_missing_equality(self):
        '''Check if the CheckGzip class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = brebis.checkbackups.checkgzip.CheckGzip({'path':
            'tests/file_size/mygzip.gz',
             'files_list':
                'tests/file_size/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'mygzip')

    def test_checkgzip_missing_bigger_than(self):
        '''Check if the CheckGzip class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than= []
        __missing_bigger_than = brebis.checkbackups.checkgzip.CheckGzip({'path':
            'tests/file_size/missing-bigger-than/mygzip.gz',
             'files_list':
                'tests/file_size/missing-bigger-than/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'mygzip')

    def test_checkgzip_missing_smaller_than(self):
        '''Check if the CheckGzip class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than= []
        __missing_smaller_than = brebis.checkbackups.checkgzip.CheckGzip({'path':
            'tests/file_size/missing-smaller-than/mygzip.gz',
             'files_list':
                'tests/file_size/missing-smaller-than/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'mygzip')

    def test_checkzip_missing_files(self):
        '''Check if the CheckZip class returns a missing file'''
        _missing_files = []
        _missing_files = brebis.checkbackups.checkzip.CheckZip({'path':
            'tests/zip/myzip.zip',
             'files_list':
                'tests/zip/myzip-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_files
        self.assertEqual(_missing_files, ['toto/bling'])

    def test_checkzip_missing_equality(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = brebis.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive', 'delimiter': ''}, Options()).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'myzip/titi')

    def test_checkzip_missing_bigger_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than= []
        __missing_bigger_than = brebis.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'myzip/foo/toto')

    def test_checkzip_missing_smaller_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than= []
        __missing_smaller_than = brebis.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive', 'delimiter': ''}, Options()).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'myzip/toutou')

##    def test_configurations(self):
##        '''Test the Configurations class'''
##        __path = os.path.abspath('tests/test_conf/')
##        __res = brebis.configurations.Configurations(__path).configs
##        self.assertEqual({'essai': {'path': os.path.normpath(os.path.join(__path,'essai.tar.gz')), 'files_list': os.path.normpath(os.path.join(__path,'essai-list')), 'type': 'archive', 'delimiter': '|'}}, __res)
##
##    def test_configurations_with_subdir(self):
##        '''Test the Configurations class with a subdirectory'''
##        __path = os.path.abspath('tests/test_conf/subdir/')
##        __res = brebis.configurations.Configurations(__path).configs
##        self.assertEqual({'essai2': {'path': os.path.normpath(os.path.join(__path, 'toto/essai.tar.gz')), 'files_list': os.path.normpath(os.path.join(__path, 'toto/essai-list')), 'type': 'archive'}}, __res)
##
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
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/expected_uid_gid/foo.tar.gz',
             'files_list':
                'tests/expected_uid_gid/files-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __uids = __myobj.mismatched_uids
        __gids = __myobj.mismatched_gids
        self.assertEqual((__uids[0],__gids[0]), (
        {'path':'foo/foo1','expecteduid':1001,'uid':1000},
        {'path':'foo/foo1','expectedgid':1001,'gid':1000}))

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
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
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

    @unittest.expectedFailure
    def test_filetree_compare_mode(self):
        '''Compare the mode of a file in the filetree and the
        expected one
        '''
        __myobj = brebis.checkbackups.checktree.CheckTree({'path':
            'tests/expected_mode/foo',
             'files_list':
                'tests/expected_mode/treefiles-list',
             'type': 'tree', 'delimiter': ''}, Options())
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'foo1','expectedmode':'664','mode':'644'},
        {'path':'bar','expectedmode':'754','mode':'755'}])

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
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
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

    @unittest.expectedFailure
    def test_filetree_compare_type(self):
        '''Compare the type of a file in the filetree and the
        expected one - expecting to fail because of special files
        '''
        __myobj = brebis.checkbackups.checktree.CheckTree({'path':
            'tests/expected_type/foos',
             'files_list':
                'tests/expected_type/filetree-list',
             'type': 'tree', 'delimiter': ''}, Options())
        __types = __myobj.mismatched_types
        self.assertEqual(__types, [
        {'path':'foos/foo2','expectedtype':'c','type':'f'},
        {'path':'foos/foo1','expectedtype':'d','type':'f'},
        {'path':'foos/foo3','expectedtype':'d','type':'f'},
        {'path':'foos/foo4','expectedtype':'s','type':'f'},
        {'path':'foos/foo6','expectedtype':'k','type':'f'},
        {'path':'foos/foo5','expectedtype':'b','type':'f'},
        {'path':'foos/bar','expectedtype':'f','type':'d'},
        {'path':'foos/bar/bar1','expectedtype':'o','type':'f'}])

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
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
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

    @unittest.expectedFailure
    def test_filetree_compare_hash(self):
        '''Compare the hash of a file in the file tree and the
        expected one - expecting to fail because of special files
        '''
        __myobj = brebis.checkbackups.checktree.CheckTree({'path':
            'tests/expected_hash/bar',
             'files_list':
                'tests/expected_hash/filetree-list',
             'type': 'tree', 'delimiter': ''}, Options())
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

    def test_zip_compare_hash(self):
        '''Compare the hash of a file in the zip archive and the
        expected one
        '''
        __myobj = brebis.checkbackups.checkzip.CheckZip({'path':
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
        __myobj = brebis.checkbackups.checkgzip.CheckGzip({'path':
            'tests/expected_hash/bar.gz',
             'files_list':
                'tests/expected_hash/gzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __hashes = __myobj.mismatched_hashes
        self.assertEqual(__hashes, [
            {'path': 'bar',
            'expectedhash': 'ede',
            'hash': 'ede69eff9660689e65c5e47bb849f152'}])

    def test_bzip2_compare_hash(self):
        '''Compare the hash of a file in the bzip2 archive and the
        expected one
        '''
        __myobj = brebis.checkbackups.checkbzip2.CheckBzip2({'path':
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
        __missing_equality = brebis.checkbackups.checktar.CheckTar({'path':
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
        __missing_smaller_than = brebis.checkbackups.checktar.CheckTar({'path':
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
        __missing_bigger_than = brebis.checkbackups.checktar.CheckTar({'path':
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
        __missing_equality = brebis.checkbackups.checkzip.CheckZip({'path':
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
        __missing_smaller_than = brebis.checkbackups.checkzip.CheckZip({'path':
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
        __missing_bigger_than = brebis.checkbackups.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/arcsize/smallerthanziparcsize-list',
             'type': 'archive', 'delimiter': ''}, Options()).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'tests/file_size/myzip.zip')

    def test_checktar_md5_hash_archive(self):
        '''Check the md5 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/md5hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': '47907de120577e6ba3b9dd8821374937',
            'hash': '47907de120577e6ba3b9dd8821374936'})

    def test_checktar_sha1_hash_archive(self):
        '''Check the sha1 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha1hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': '84db203e2902fa5ea51e6d46ea365c7bfc5524b9',
            'hash': '84db203e2902fa5ea51e6d46ea365c7bfc5524b8'})

    def test_checktar_sha224_hash_archive(self):
        '''Check the sha224 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha224hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': 'e25621dfdd2b2cfca451c735f4e676653e8628187e2b7ddc14402c1e',
            'hash': 'e25621dfdd2b2cfca451c735f4e676653e8628187e2b7ddc14402c1d'})

    def test_checktar_sha256_hash_archive(self):
        '''Check the sha256 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha256hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': '7090d29295216e95ab4a190d489aa405d141cac978567c227f17ee78eb3f5fd5',
            'hash': '7090d29295216e95ab4a190d489aa405d141cac978567c227f17ee78eb3f5fd4'})

    def test_checktar_sha384_hash_archive(self):
        '''Check the sha384 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha384hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': 'aa01a55142a04de52cebba3797ca25054e51c33a5fbfdc4dd0cc2f01f6252c6a62cb87f35405d9d8b07a506eefacfd11',
            'hash': 'aa01a55142a04de52cebba3797ca25054e51c33a5fbfdc4dd0cc2f01f6252c6a62cb87f35405d9d8b07a506eefacfd10'})

    def test_checktar_sha512_hash_archive(self):
        '''Check the sha512 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkbackups.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha512hashtararchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': 'd72eef1d9c42615f6b2a92848e8fa65ffd4276d91d9976fa8c644b41c15d91441ae42f897b30a2403795a876b14ae6ed8addca4a74f24839f6506a29e662e588',
            'hash': 'd72eef1d9c42615f6b2a92848e8fa65ffd4276d91d9976fa8c644b41c15d91441ae42f897b30a2403795a876b14ae6ed8addca4a74f24839f6506a29e662e587'})

    def test_checkzip_md5_hash_archive(self):
        '''Check the md5 hash of the zip archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/md5hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': 'e48e1ce2fbe0db616632ba8030ac2c9e',
            'hash': 'e48e1ce2fbe0db616632ba8030ac2c9f'})

    def test_checkzip_sha1_hash_archive(self):
        '''Check the sha1 hash of the zip archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha1hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '4cd5933d78603d8b4ba484ef8e45d2b6bc9fd5ce',
            'hash': '4cd5933d78603d8b4ba484ef8e45d2b6bc9fd5cf'})

    def test_checkzip_sha224_hash_archive(self):
        '''Check the sha224 hash of the zip archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha224hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '6e0838302f48cc7863a160f197a23492833b59862d89cabc46c2a1c4',
            'hash': '6e0838302f48cc7863a160f197a23492833b59862d89cabc46c2a1c3'})

    def test_checkzip_sha256_hash_archive(self):
        '''Check the sha256 hash of the zip archive itself using CheckZip class'''
        __mismatchedhashes = brebis.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha256hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '358bae9af3f9f510095b2e2a245a5e49ab27d7de862cd22f0dd4f212e25fb139',
            'hash': '358bae9af3f9f510095b2e2a245a5e49ab27d7de862cd22f0dd4f212e25fb138'})

    def test_checkzip_sha384_hash_archive(self):
        '''Check the sha384 hash of the zip archive itself using CheckZip class'''
        __mismatchedhashes = brebis.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha384hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '6a372e2867442826b64d1e3bca4b35e18d12d5df25e89decff214023d45f7f85d07ee79e6522f53961626e525ee29988',
            'hash': '6a372e2867442826b64d1e3bca4b35e18d12d5df25e89decff214023d45f7f85d07ee79e6522f53961626e525ee29989'})

    def test_checkzip_sha512_hash_archive(self):
        '''Check the sha512 hash of the zip archive itself using CheckZip class'''
        __mismatchedhashes = brebis.checkbackups.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha512hashziparchive-list',
         'type': 'archive', 'delimiter': ''}, Options()).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': 'c177ca5b618ca613f27c44991eabb922d589691000fa602a0d2767ba84b317c653e6ed541f5922d201d2e65158eee4cfb7d87665bbe1d31c07f636bb25dac7b2',
            'hash': 'c177ca5b618ca613f27c44991eabb922d589691000fa602a0d2767ba84b317c653e6ed541f5922d201d2e65158eee4cfb7d87665bbe1d31c07f636bb25dac7b3'})

    @unittest.expectedFailure
    def test_tar_archive_compare_644_mode(self):
        '''Compare the 644 mode of the tar archive and the
        expected one
        '''
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/expected_mode/arcmode/mode644.tar.gz',
             'files_list':
                'tests/expected_mode/arcmode/tarmode644-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode644.tar.gz','expectedmode':'654','mode':'644'}])

    @unittest.expectedFailure
    def test_tar_archive_compare_755_mode(self):
        '''Compare the 755 mode of the tar archive and the
        expected one
        '''
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/expected_mode/arcmode/mode755.tar.gz',
             'files_list':
                'tests/expected_mode/arcmode/tarmode755-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode755.tar.gz','expectedmode':'750','mode':'755'}])

    @unittest.expectedFailure
    def test_tar_archive_compare_4644_mode(self):
        '''Compare the 4644 mode of the tar archive and the
        expected one - expecting to fail because of the sticky bit
        '''
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/expected_mode/arcmode/mode4644.tar.gz',
             'files_list':
                'tests/expected_mode/arcmode/tarmode4644-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode4644.tar.gz','expectedmode':'4600','mode':'4644'}])

    @unittest.expectedFailure
    def test_zip_archive_compare_644_mode(self):
        '''Compare the 644 mode of the zip archive and the
        expected one
        '''
        __myobj = brebis.checkbackups.checkzip.CheckZip({'path':
            'tests/expected_mode/arcmode/mode644.zip',
             'files_list':
                'tests/expected_mode/arcmode/zipmode644-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode644.zip','expectedmode':'654','mode':'644'}])

    @unittest.expectedFailure
    def test_zip_archive_compare_755_mode(self):
        '''Compare the 755 mode of the zip archive and the
        expected one
        '''
        __myobj = brebis.checkbackups.checkzip.CheckZip({'path':
            'tests/expected_mode/arcmode/mode755.zip',
             'files_list':
                'tests/expected_mode/arcmode/zipmode755-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode755.zip','expectedmode':'750','mode':'755'}])

    @unittest.expectedFailure
    def test_zip_archive_compare_4644_mode(self):
        '''Compare the 4644 mode of the zip archive and the
        expected one - expecting to fail because of the sticky bit
        '''
        __myobj = brebis.checkbackups.checkzip.CheckZip({'path':
            'tests/expected_mode/arcmode/mode4644.zip',
             'files_list':
                'tests/expected_mode/arcmode/zipmode4644-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode4644.zip','expectedmode':'4600','mode':'4644'}])

    def test_compare_tar_archive_uid_gid(self):
        '''Compare the uid and the gid of the tar archive itself
        and the expected one
        '''
        __uids = []
        __gids = []
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
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
        __myobj = brebis.checkbackups.checkzip.CheckZip({'path':
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
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __fileinfo = __myobj._CheckArchive__extract_archive_info(__file)
        self.assertEqual(type(os.lstat(__file)), type(__fileinfo))

    def test_find_archive_size(self):
        '''test the find_archive_size private method from CheckArchive'''
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __filesize = __myobj._CheckArchive__find_archive_size(__file)
        self.assertEqual(os.lstat(__file).st_size, __filesize)

    def test_find_archive_mode(self):
        '''test the find_archive_mode private method from CheckArchive'''
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __filemode = __myobj._CheckArchive__find_archive_mode(__file)
        self.assertEqual(stat.S_IMODE(os.lstat(__file).st_mode), __filemode)

    def test_find_archive_uid_gid(self):
        '''test the find_archive_uid_gid private method from CheckArchive'''
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __arcuid, __arcgid = __myobj._CheckArchive__find_archive_uid_gid(__file)
        __fileinfo = os.lstat(__file)
        __fileuid, __filegid = __fileinfo.st_uid, __fileinfo.st_gid
        self.assertEqual((__arcuid, __arcgid), (__fileuid, __filegid))

##############################################################
#
# Testing the private/protected methods from checkzip.CheckZip 
#
##############################################################

    def test_zip_extract_stored_file(self):
        '''test the _extract_stored_file protected method from checkzip.CheckZip'''
        __myobj = brebis.checkbackups.checkzip.CheckZip({'path':
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
        __myobj = brebis.checkbackups.checkzip.CheckZip({'path':
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
        __myobj = brebis.checkbackups.checkzip.CheckZip({'path':
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
        __myobj = brebis.checkbackups.checkzip.CheckZip({'path':
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
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
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
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
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
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
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
        __myobj = brebis.checkbackups.checktar.CheckTar({'path':
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
        __myobj = brebis.checkbackups.checktree.CheckTree({'path':
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
        __myobj = brebis.checkbackups.checktree.CheckTree({'path':
            'tests/checktree_private_methods/mytree',
             'files_list':
                'tests/checktree_private_methods/mytree-list',
             'type': 'tree', 'delimiter': ''}, Options())
        __file = 'tests/checktree_private_methods/mytree/hello'
        __result = __myobj._CheckTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('f', __result)

    def test_tree_translate_type_directory(self):
        '''test the __translate_type private method from checktree.CheckTree - expecting directory'''
        __myobj = brebis.checkbackups.checktree.CheckTree({'path':
            'tests/checktree_private_methods/mytree',
             'files_list':
                'tests/checktree_private_methods/mytree-list',
             'type': 'tree', 'delimiter': ''}, Options())
        __file = 'tests/checktree_private_methods/mytree'
        __result = __myobj._CheckTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('d', __result)

    def test_tree_translate_type_symbolic_link(self):
        '''test the __translate_type private method from checktree.CheckTree - expecting symbolic link'''
        __myobj = brebis.checkbackups.checktree.CheckTree({'path':
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
        __myobj = brebis.checkbackups.checkgzip.CheckGzip({'path':
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
        __myobj = brebis.checkbackups.checkgzip.CheckGzip({'path':
            __arcpath,
             'files_list':
                'tests/checkgzip_private_methods/mygzip-list',
             'type': 'archive', 'delimiter': ''}, Options())
        with open(__arcpath, 'rb') as __myf:
            self.assertEqual(23, __myobj._CheckGzip__extract_size(__myf))

    def test_extract_initial_filename_from_gzip_archive(self):
        '''test the extraction of the initial name of an uncompressed file'''
        __arcpath = 'tests/checkgzip_private_methods/mygzip.gz'
        __myobj = brebis.checkbackups.checkgzip.CheckGzip({'path':
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
        __myobj = brebis.checkbackups.checkbzip2.CheckBzip2({'path':
            'tests/checkbzip2_private_methods/mybz2.bz2',
             'files_list':
                'tests/checkbzip2_private_methods/mybzip2-list',
             'type': 'archive', 'delimiter': ''}, Options())
        __file = 'tests/checkbzip2_private_methods/mybz2.bz2'
        __result = __myobj._extract_stored_file('mygzip')
        with bz2.BZ2File(__file, 'r') as self.__desc:
            self.assertEqual(type(__result), type(self.__desc))
            __result.close()

###############################################################################################
#
# Testing the private/protected methods from generatelist.generatelist.GenerateList 
#
###############################################################################################

    def test_generatelist_generate_list(self):
        '''test the _generate_list protected method from GenerateList'''
        __file = 'tests/generatelist_private_methods/mytar.list'
        __myobj = brebis.generatelist.generatelist.GenerateList()
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
        __myobj = brebis.generatelist.generatelistfortar.GenerateListForTar({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
        self.__tar = tarfile.open(__file)
        __result = __myobj._GenerateListForTar__translate_type(self.__tar.getmembers()[3].type)
        self.assertEqual('f', __result)

    def test_listfortar_translate_type_directory(self):
        '''test the __translate_type private method from GenerateListForTar - expecting directory'''
        __file = 'tests/generatelistfortar_private_methods/mytar.tar.gz'
        __myobj = brebis.generatelist.generatelistfortar.GenerateListForTar({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
        self.__tar = tarfile.open(__file)
        __result = __myobj._GenerateListForTar__translate_type(self.__tar.getmembers()[1].type)
        self.assertEqual('d', __result)

    def test_listfortar_translate_type_symbolic_link(self):
        '''test the __translate_type private method from GenerateListForTar - expecting symbolic link'''
        __file = 'tests/generatelistfortar_private_methods/mytar.tar.gz'
        __myobj = brebis.generatelist.generatelistfortar.GenerateListForTar({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
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
        __myobj = brebis.generatelist.generatelistforzip.GenerateListForZip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._GenerateListForZip__translate_type(__myinfo[-1].external_attr >> 16)
        self.assertEqual('f', __result)

    def test_listforzip_translate_type_directory(self):
        '''test the __translate_type private method from GenerateListForZip - expecting directory'''
        __file = 'tests/generatelistforzip_private_methods/myzip.zip'
        __myobj = brebis.generatelist.generatelistforzip.GenerateListForZip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._GenerateListForZip__translate_type(__myinfo[0].external_attr >> 16)
        self.assertEqual('d', __result)

    def test_listforzip_extract_uid_gid(self):
        '''test the __extract_uid_gid private method from GenerateListForZip'''
        __file = 'tests/generatelistforzip_private_methods/myzip.zip'
        __myobj = brebis.generatelist.generatelistforzip.GenerateListForZip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
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
        __myobj = brebis.generatelist.generatelistfortree.GenerateListForTree({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
        __result = __myobj._GenerateListForTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('f', __result)

    def test_listfortree_translate_type_directory(self):
        '''test the __translate_type private method from GenerateListForTree - expecting directory'''
        __dir = 'tests/generatelistfortree_private_methods/mydir'
        __file = os.path.join(__dir, 'bar')
        __myobj = brebis.generatelist.generatelistfortree.GenerateListForTree({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
        __result = __myobj._GenerateListForTree__translate_type(os.lstat(__file).st_mode)
        self.assertEqual('d', __result)

    def test_listfortree_translate_type_symbolic_link(self):
        '''test the __translate_type private method from GenerateListForTree - expecting symbolic link'''
        __dir = 'tests/generatelistfortree_private_methods/mydir'
        __file = os.path.join(__dir, 'oof')
        __myobj = brebis.generatelist.generatelistfortree.GenerateListForTree({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
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
        __myobj = brebis.generatelist.generatelistforgzip.GenerateListForGzip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
        with open(__file, 'rb') as __myf:
            self.assertEqual(15, __myobj._GenerateListForGzip__extract_size(__myf))

    def test_listforgzip_extract_initial_filename_from_gzip_archive(self):
        __file = 'tests/generatelistforgzip_private_methods/mygzip.gz'
        __myobj = brebis.generatelist.generatelistforgzip.GenerateListForGzip({'arcpath':__file, 'delimiter':DEFAULTDELIMITER, 'genfull':False})
        with open(__file, 'rb') as __myf:
            self.assertEqual('mygzip', __myobj._GenerateListForGzip__extract_initial_filename(__myf, 'mygzip'))

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
        with open('brebis/cliparse.py') as __cliparsepy:
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

################################################################
#
# End of the unit tests
#
################################################################
if __name__ == '__main__':
    unittest.main()
