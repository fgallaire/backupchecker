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

import os
import os.path
import stat
import logging
import sys
import unittest
import zipfile

import brebis.applogger
import brebis.checkbackups
import brebis.checkhashes
import brebis.checktar
import brebis.checktree
import brebis.checkzip
import brebis.cliparse
import brebis.configurations
import brebis.checkarchive
from brebis.expectedvalues import ExpectedValues
import brebis.main

# !! logging module uses a single logger for the whole file
TESTLOG = 'tests/testlog'

class TestApp(unittest.TestCase):

    def test_applogger(self):
        '''Test the AppLoggerclass'''
        brebis.applogger.AppLogger(TESTLOG)
        self.assertEqual(True, str(logging.getLogger('applogger')).startswith('<logging.Logger object at'))
        
    def test_checkbackup(self):
        '''Test the CheckBackup class'''
        _logfile = TESTLOG
        brebis.applogger.AppLogger(_logfile)
        brebis.checkbackups.CheckBackups({'essai': {'path': 'tests/tar_gz_archive_content/essai.tar.gz', 'files_list': 'tests/tar_gz_archive_content/essai-list', 'type': 'archive'}, 'essai2': {'path': 'tests/tar_bz2_archive_content/titi.tar.bz2', 'files_list': 'tests/tar_bz2_archive_content/essai2-list', 'type': 'archive'}})
        with open(_logfile) as _res:
            self.assertEqual(_res.read(), 'WARNING:root:1 file missing in tests/tar_gz_archive_content/essai.tar.gz: \nWARNING:root:essai/dir/titi\n')
        os.remove(_logfile)

    def test_checkhashes_md5(self):
        '''Test the CheckHashes class with MD5'''
        _hashfile = 'tests/corrupted_archives/MD5SUMS'
        _hashtype = 'md5'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/md5-corrupted.tar.gz', 'type': 'archive'}}
        __checker = brebis.checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha1(self):
        '''Test the CheckHashes class with SHA1'''
        _hashfile = 'tests/corrupted_archives/SHA1SUMS'
        _hashtype = 'sha1'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha1-corrupted.tar.gz', 'type': 'archive'}}
        __checker = brebis.checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha224(self):
        '''Test the CheckHashes class with SHA224'''
        _hashfile = 'tests/corrupted_archives/SHA224SUMS'
        _hashtype = 'sha224'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha224-corrupted.tar.bz2', 'type': 'archive'}}
        __checker = brebis.checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha256(self):
        '''Test the CheckHashes class with SHA256'''
        _hashfile = 'tests/corrupted_archives/SHA256SUMS'
        _hashtype = 'sha256'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha256-corrupted.tar.gz', 'type': 'archive'}}
        __checker = brebis.checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha384(self):
        '''Test the CheckHashes class with SHA384'''
        _hashfile = 'tests/corrupted_archives/SHA384SUMS'
        _hashtype = 'sha384'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha384-corrupted.tar.bz2', 'type': 'archive'}}
        __checker = brebis.checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha512(self):
        '''Test the CheckHashes class with SHA512'''
        _hashfile = 'tests/corrupted_archives/SHA512SUMS'
        _hashtype = 'sha512'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha512-corrupted.tar.gz', 'type': 'archive'}}
        __checker = brebis.checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checktar_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        _missingfiles = []
        _missingfiles = brebis.checktar.CheckTar({'path':
            'tests/tar_gz_archive_content/essai.tar.gz',
             'files_list':
                'tests/tar_gz_archive_content/essai-list',
             'type': 'archive'}).missing_files
        self.assertEqual(_missingfiles, ['essai/dir/titi'])

    def test_checktar_missing_equality(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = brebis.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'essai/dir/toto')

    def test_checktar_missing_bigger_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = brebis.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'essai/titi')

    def test_checktar_missing_smaller_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = brebis.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'essai/dir/toutou')

    def test_checktree_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        __missing_files = []
        __missing_files = brebis.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_files
        self.assertEqual(__missing_files, ['bar/toto'])

    def test_checktree_missing_equality(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality= []
        __missing_equality = brebis.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'foo1')

    def test_checktree_missing_bigger_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = brebis.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'foo2')

    def test_checktree_missing_smaller_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = brebis.checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'bar/foo3')

    def test_checkzip_missing_files(self):
        '''Check if the CheckZip class returns a missing file'''
        _missing_files = []
        _missing_files = brebis.checkzip.CheckZip({'path':
            'tests/zip/myzip.zip',
             'files_list':
                'tests/zip/myzip-list',
             'type': 'archive'}).missing_files
        self.assertEqual(_missing_files, ['toto/bling'])

    def test_checkzip_missing_equality(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = brebis.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'myzip/titi')

    def test_checkzip_missing_bigger_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than= []
        __missing_bigger_than = brebis.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'myzip/foo/toto')

    def test_checkzip_missing_smaller_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than= []
        __missing_smaller_than = brebis.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'myzip/toutou')

    def test_configurations(self):
        '''Test the Configurations class'''
        __path = os.path.abspath('tests/test_conf/')
        __res = brebis.configurations.Configurations(__path).configs
        self.assertEqual({'essai': {'path': os.path.normpath(os.path.join(__path,'essai.tar.gz')), 'files_list': os.path.normpath(os.path.join(__path,'essai-list')), 'type': 'archive'}}, __res)

    def test_configurations_with_subdir(self):
        '''Test the Configurations class with a subdirectory'''
        __path = os.path.abspath('tests/test_conf/subdir/')
        __res = brebis.configurations.Configurations(__path).configs
        self.assertEqual({'essai2': {'path': os.path.normpath(os.path.join(__path, 'toto/essai.tar.gz')), 'files_list': os.path.normpath(os.path.join(__path, 'toto/essai-list')), 'type': 'archive'}}, __res)

    def test_expected_values(self):
        '''Check the ExpectedValues class'''
        __data, _ = ExpectedValues('tests/file_size/essai-list').data
        self.assertEqual([{'path':'essai/dir/toto', 'equals':536870912},
            {'path':'essai/titi','biggerthan':536870912},
            {'path':'essai/dir/toutou','smallerthan':19},
            {'path':'essai/dir/zozo'}], __data)

    def test_unexpected_files(self):
        '''Check if an unexpected file is identified'''
        __data, _ = ExpectedValues('tests/unexpected_files/files-list').data
        self.assertEqual([{'path':'foo/foo1'},{'path':'foo/foo2'},
            {'path':'foo/bar','unexpected':True}], __data)

    def test_extract_expected_uid_gid(self):
        '''Check the uid and gid of an expected file''' 
        __data, _ = ExpectedValues('tests/expected_uid_gid/files-list').data
        self.assertEqual([{'path':'foo/foo1', 'uid':1001, 'gid':1001}], __data)

    def test_compare_uid_gid(self):
        '''Compare the uid and the gid of a file in the archive
        and the expected one
        '''
        __uids = []
        __gids = []
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/expected_uid_gid/foo.tar.gz',
             'files_list':
                'tests/expected_uid_gid/files-list',
             'type': 'archive'})
        __uids = __myobj.mismatched_uids
        __gids = __myobj.mismatched_gids
        self.assertEqual((__uids[0],__gids[0]), (
        {'path':'foo/foo1','expecteduid':1001,'uid':1000},
        {'path':'foo/foo1','expectedgid':1001,'gid':1000}))

    def test_extract_modes(self):
        '''Extract the expected file modes'''
        __data, _ = ExpectedValues('tests/expected_mode/files-list').data
        self.assertEqual([{'path':'foos/foo1', 'mode': '644'},
            {'path':'foos/foo2', 'mode': '755'},
            {'path':'foos/bar/foo3', 'mode': '4644'},
            {'path':'foos/bar', 'mode': '754'}], __data)

    def test_archive_compare_mode(self):
        '''Compare the mode of a file in the archive and the
        expected one
        '''
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/expected_mode/foos.tar.gz',
             'files_list':
                'tests/expected_mode/files-list',
             'type': 'archive'})
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'foos/foo2','expectedmode':'755','mode':'754'},
        {'path':'foos/bar','expectedmode':'754','mode':'755'},
        {'path':'foos/bar/foo3','expectedmode':'4644','mode':'4600'},
        {'path':'foos/foo1','expectedmode':'644','mode':'744'}])

    def test_filetree_compare_mode(self):
        '''Compare the mode of a file in the filetree and the
        expected one
        '''
        __myobj = brebis.checktree.CheckTree({'path':
            'tests/expected_mode/foo',
             'files_list':
                'tests/expected_mode/treefiles-list',
             'type': 'tree'})
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'foo1','expectedmode':'664','mode':'644'},
        {'path':'bar','expectedmode':'754','mode':'755'}])

    def test_extract_types(self):
        '''Extract the expected file types'''
        __data, _ = ExpectedValues('tests/expected_type/files-list').data
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
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/expected_type/foos.tar.gz',
             'files_list':
                'tests/expected_type/files-list',
             'type': 'archive'})
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
        __myobj = brebis.checktree.CheckTree({'path':
            'tests/expected_type/foos',
             'files_list':
                'tests/expected_type/filetree-list',
             'type': 'tree'})
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
        __data, _ = ExpectedValues('tests/expected_hash/files-list').data
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
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/expected_hash/foos.tar.gz',
             'files_list':
                'tests/expected_hash/files-list',
             'type': 'archive'})
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
        __myobj = brebis.checktree.CheckTree({'path':
            'tests/expected_hash/bar',
             'files_list':
                'tests/expected_hash/filetree-list',
             'type': 'tree'})
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
        __myobj = brebis.checkzip.CheckZip({'path':
            'tests/expected_hash/bar.zip',
             'files_list':
                'tests/expected_hash/zip-list',
             'type': 'archive'})
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

    def test_checktar_archive_equal_size(self):
        '''Check if the CheckTar class returns a dictionary with the
           archive itself file whose size should have been equal
           to the expected size.
        '''
        __missing_equality = []
        __missing_equality = brebis.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/arcsize/equaltararcsize-list',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'tests/file_size/essai.tar.bz2')
        
    def test_checktar_archive_missing_smaller_than(self):
        '''Check if the CheckTar class returns a dictionary with the
           archive itself whose size should have been smaller 
           than the expected size.
        '''
        __missing_smaller_than = []
        __missing_smaller_than = brebis.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/arcsize/biggerthantararcsize-list',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'tests/file_size/essai.tar.bz2')

    def test_checktar_archive_missing_bigger_than(self):
        '''Check if the CheckTar class returns a dictionary with the
           archive itself whose size should have been bigger 
           than the expected size.
        '''
        __missing_bigger_than = []
        __missing_bigger_than = brebis.checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/arcsize/smallerthantararcsize-list',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'tests/file_size/essai.tar.bz2')

    def test_checkzip_archive_equal_size(self):
        '''Check if the CheckZip class returns a dictionary with the
           archive itself file whose size should have been equal
           to the expected size.
        '''
        __missing_equality = []
        __missing_equality = brebis.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/arcsize/equalziparcsize-list',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'tests/file_size/myzip.zip')
        
    def test_checkzip_archive_missing_smaller_than(self):
        '''Check if the CheckZip class returns a dictionary with the
           archive itself whose size should have been smaller 
           than the expected size.
        '''
        __missing_smaller_than = []
        __missing_smaller_than = brebis.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/arcsize/biggerthanziparcsize-list',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'tests/file_size/myzip.zip')

    def test_checkzip_archive_missing_bigger_than(self):
        '''Check if the CheckZip class returns a dictionary with the
           archive itself whose size should have been bigger 
           than the expected size.
        '''
        __missing_bigger_than = []
        __missing_bigger_than = brebis.checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/arcsize/smallerthanziparcsize-list',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'tests/file_size/myzip.zip')

    def test_checktar_md5_hash_archive(self):
        '''Check the md5 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/md5hashtararchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': '47907de120577e6ba3b9dd8821374937',
            'hash': '47907de120577e6ba3b9dd8821374936'})

    def test_checktar_sha1_hash_archive(self):
        '''Check the sha1 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha1hashtararchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': '84db203e2902fa5ea51e6d46ea365c7bfc5524b9',
            'hash': '84db203e2902fa5ea51e6d46ea365c7bfc5524b8'})

    def test_checktar_sha224_hash_archive(self):
        '''Check the sha224 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha224hashtararchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': 'e25621dfdd2b2cfca451c735f4e676653e8628187e2b7ddc14402c1e',
            'hash': 'e25621dfdd2b2cfca451c735f4e676653e8628187e2b7ddc14402c1d'})

    def test_checktar_sha256_hash_archive(self):
        '''Check the sha256 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha256hashtararchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': '7090d29295216e95ab4a190d489aa405d141cac978567c227f17ee78eb3f5fd5',
            'hash': '7090d29295216e95ab4a190d489aa405d141cac978567c227f17ee78eb3f5fd4'})

    def test_checktar_sha384_hash_archive(self):
        '''Check the sha384 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha384hashtararchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': 'aa01a55142a04de52cebba3797ca25054e51c33a5fbfdc4dd0cc2f01f6252c6a62cb87f35405d9d8b07a506eefacfd11',
            'hash': 'aa01a55142a04de52cebba3797ca25054e51c33a5fbfdc4dd0cc2f01f6252c6a62cb87f35405d9d8b07a506eefacfd10'})

    def test_checktar_sha512_hash_archive(self):
        '''Check the sha512 hash of the tar archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checktar.CheckTar({'path':
        'tests/expected_hash/archash/mytar.tar.gz',
         'files_list':
            'tests/expected_hash/archash/sha512hashtararchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/mytar.tar.gz',
            'expectedhash': 'd72eef1d9c42615f6b2a92848e8fa65ffd4276d91d9976fa8c644b41c15d91441ae42f897b30a2403795a876b14ae6ed8addca4a74f24839f6506a29e662e588',
            'hash': 'd72eef1d9c42615f6b2a92848e8fa65ffd4276d91d9976fa8c644b41c15d91441ae42f897b30a2403795a876b14ae6ed8addca4a74f24839f6506a29e662e587'})

    def test_checkzip_md5_hash_archive(self):
        '''Check the md5 hash of the zip archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/md5hashziparchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': 'e48e1ce2fbe0db616632ba8030ac2c9e',
            'hash': 'e48e1ce2fbe0db616632ba8030ac2c9f'})

    def test_checkzip_sha1_hash_archive(self):
        '''Check the sha1 hash of the zip archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha1hashziparchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '4cd5933d78603d8b4ba484ef8e45d2b6bc9fd5ce',
            'hash': '4cd5933d78603d8b4ba484ef8e45d2b6bc9fd5cf'})

    def test_checkzip_sha224_hash_archive(self):
        '''Check the sha224 hash of the zip archive itself using CheckTar class'''
        __mismatchedhashes = brebis.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha224hashziparchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '6e0838302f48cc7863a160f197a23492833b59862d89cabc46c2a1c4',
            'hash': '6e0838302f48cc7863a160f197a23492833b59862d89cabc46c2a1c3'})

    def test_checkzip_sha256_hash_archive(self):
        '''Check the sha256 hash of the zip archive itself using CheckZip class'''
        __mismatchedhashes = brebis.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha256hashziparchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '358bae9af3f9f510095b2e2a245a5e49ab27d7de862cd22f0dd4f212e25fb139',
            'hash': '358bae9af3f9f510095b2e2a245a5e49ab27d7de862cd22f0dd4f212e25fb138'})

    def test_checkzip_sha384_hash_archive(self):
        '''Check the sha384 hash of the zip archive itself using CheckZip class'''
        __mismatchedhashes = brebis.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha384hashziparchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': '6a372e2867442826b64d1e3bca4b35e18d12d5df25e89decff214023d45f7f85d07ee79e6522f53961626e525ee29988',
            'hash': '6a372e2867442826b64d1e3bca4b35e18d12d5df25e89decff214023d45f7f85d07ee79e6522f53961626e525ee29989'})

    def test_checkzip_sha512_hash_archive(self):
        '''Check the sha512 hash of the zip archive itself using CheckZip class'''
        __mismatchedhashes = brebis.checkzip.CheckZip({'path':
        'tests/expected_hash/archash/myzip.zip',
         'files_list':
            'tests/expected_hash/archash/sha512hashziparchive-list',
         'type': 'archive'}).mismatched_hashes
        self.assertEqual(__mismatchedhashes[0], {'path': 'tests/expected_hash/archash/myzip.zip',
            'expectedhash': 'c177ca5b618ca613f27c44991eabb922d589691000fa602a0d2767ba84b317c653e6ed541f5922d201d2e65158eee4cfb7d87665bbe1d31c07f636bb25dac7b2',
            'hash': 'c177ca5b618ca613f27c44991eabb922d589691000fa602a0d2767ba84b317c653e6ed541f5922d201d2e65158eee4cfb7d87665bbe1d31c07f636bb25dac7b3'})

    def test_tar_archive_compare_644_mode(self):
        '''Compare the 644 mode of the tar archive and the
        expected one
        '''
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/expected_mode/arcmode/mode644.tar.gz',
             'files_list':
                'tests/expected_mode/arcmode/tarmode644-list',
             'type': 'archive'})
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode644.tar.gz','expectedmode':'654','mode':'644'}])

    def test_tar_archive_compare_755_mode(self):
        '''Compare the 755 mode of the tar archive and the
        expected one
        '''
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/expected_mode/arcmode/mode755.tar.gz',
             'files_list':
                'tests/expected_mode/arcmode/tarmode755-list',
             'type': 'archive'})
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode755.tar.gz','expectedmode':'750','mode':'755'}])

    @unittest.expectedFailure
    def test_tar_archive_compare_4644_mode(self):
        '''Compare the 4644 mode of the tar archive and the
        expected one - expecting to fail because of the sticky bit
        '''
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/expected_mode/arcmode/mode4644.tar.gz',
             'files_list':
                'tests/expected_mode/arcmode/tarmode4644-list',
             'type': 'archive'})
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode4644.tar.gz','expectedmode':'4600','mode':'4644'}])

    def test_zip_archive_compare_644_mode(self):
        '''Compare the 644 mode of the zip archive and the
        expected one
        '''
        __myobj = brebis.checkzip.CheckZip({'path':
            'tests/expected_mode/arcmode/mode644.zip',
             'files_list':
                'tests/expected_mode/arcmode/zipmode644-list',
             'type': 'archive'})
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode644.zip','expectedmode':'654','mode':'644'}])

    def test_zip_archive_compare_755_mode(self):
        '''Compare the 755 mode of the zip archive and the
        expected one
        '''
        __myobj = brebis.checkzip.CheckZip({'path':
            'tests/expected_mode/arcmode/mode755.zip',
             'files_list':
                'tests/expected_mode/arcmode/zipmode755-list',
             'type': 'archive'})
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode755.zip','expectedmode':'750','mode':'755'}])

    @unittest.expectedFailure
    def test_zip_archive_compare_4644_mode(self):
        '''Compare the 4644 mode of the zip archive and the
        expected one - expecting to fail because of the sticky bit
        '''
        __myobj = brebis.checkzip.CheckZip({'path':
            'tests/expected_mode/arcmode/mode4644.zip',
             'files_list':
                'tests/expected_mode/arcmode/zipmode4644-list',
             'type': 'archive'})
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'tests/expected_mode/arcmode/mode4644.zip','expectedmode':'4600','mode':'4644'}])

    def test_compare_tar_archive_uid_gid(self):
        '''Compare the uid and the gid of the tar archive itself
        and the expected one
        '''
        __uids = []
        __gids = []
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/expected_uid_gid/arc_uid_gid/uid-gid.tar.gz',
             'files_list':
                'tests/expected_uid_gid/arc_uid_gid/tar-uid-gid-list',
             'type': 'archive'})
        __uids = __myobj.mismatched_uids
        __gids = __myobj.mismatched_gids
        self.assertEqual((__uids[0],__gids[0]), (
        {'path':'tests/expected_uid_gid/arc_uid_gid/uid-gid.tar.gz','expecteduid':5,'uid':1000},
        {'path':'tests/expected_uid_gid/arc_uid_gid/uid-gid.tar.gz','expectedgid':6,'gid':1000}))

    def test_compare_zip_archive_uid_gid(self):
        '''Compare the uid and the gid of the zip archive itself
        and the expected one
        '''
        __uids = []
        __gids = []
        __myobj = brebis.checkzip.CheckZip({'path':
            'tests/expected_uid_gid/arc_uid_gid/uid-gid.zip',
             'files_list':
                'tests/expected_uid_gid/arc_uid_gid/zip-uid-gid-list',
             'type': 'archive'})
        __uids = __myobj.mismatched_uids
        __gids = __myobj.mismatched_gids
        self.assertEqual((__uids[0],__gids[0]), (
        {'path':'tests/expected_uid_gid/arc_uid_gid/uid-gid.zip','expecteduid':5,'uid':1000},
        {'path':'tests/expected_uid_gid/arc_uid_gid/uid-gid.zip','expectedgid':6,'gid':1000}))

###########################################################
#
# Testing the private method from checkarchive.CheckArchive
#
###########################################################

    def test_extract_archive_info(self):
        '''test the extract_archive_info private method from CheckArchive'''
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive'})
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __fileinfo = __myobj._CheckArchive__extract_archive_info(__file)
        self.assertEqual(type(os.stat(__file)), type(__fileinfo))

    def test_find_archive_size(self):
        '''test the find_archive_size private method from CheckArchive'''
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive'})
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __filesize = __myobj._CheckArchive__find_archive_size(__file)
        self.assertEqual(os.stat(__file).st_size, __filesize)

    def test_find_archive_mode(self):
        '''test the find_archive_mode private method from CheckArchive'''
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive'})
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __filemode = __myobj._CheckArchive__find_archive_mode(__file)
        self.assertEqual(stat.S_IMODE(os.stat(__file).st_mode), __filemode)

    def test_find_archive_uid_gid(self):
        '''test the find_archive_uid_gid private method from CheckArchive'''
        __myobj = brebis.checktar.CheckTar({'path':
            'tests/checkarchive_private_methods/mytar.tar.gz',
             'files_list':
                'tests/checkarchive_private_methods/tar-list',
             'type': 'archive'})
        __file = 'tests/checkarchive_private_methods/mytar.tar.gz'
        __arcuid, __arcgid = __myobj._CheckArchive__find_archive_uid_gid(__file)
        __fileinfo = os.stat(__file)
        __fileuid, __filegid = __fileinfo.st_uid, __fileinfo.st_gid
        self.assertEqual((__arcuid, __arcgid), (__fileuid, __filegid))

###########################################################
#
# Testing the private methods from checkzip.CheckZip 
#
###########################################################

    def test_translate_type_directory(self):
        '''test the __translate_type private method from CheckZip - expecting file'''
        __myobj = brebis.checkzip.CheckZip({'path':
            'tests/checkzip_private_methods/myzip.zip',
             'files_list':
                'tests/checkzip_private_methods/myzip-list',
             'type': 'archive'})
        __file = 'tests/checkzip_private_methods/myzip.zip'
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._CheckZip__translate_type(__myinfo[-1].external_attr >> 16)
        self.assertEqual('f', __result)

    def test_translate_type_file(self):
        '''test the __translate_type private method from CheckZip - expecting directory'''
        __myobj = brebis.checkzip.CheckZip({'path':
            'tests/checkzip_private_methods/myzip.zip',
             'files_list':
                'tests/checkzip_private_methods/myzip-list',
             'type': 'archive'})
        __file = 'tests/checkzip_private_methods/myzip.zip'
        __myz = zipfile.ZipFile(__file,'r')
        __myinfo = __myz.infolist()
        __result = __myobj._CheckZip__translate_type(__myinfo[0].external_attr >> 16)
        self.assertEqual('d', __result)

if __name__ == '__main__':
    unittest.main()
