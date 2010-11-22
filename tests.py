#!/usr/bin/python3

import os
import logging
import sys
import unittest

import applogger
import checkbackups
import checkhashes
import checktar
import checktree
import checkzip
import cliparse
import configurations
from expectedfiles import ExpectedFiles
import main

# !! logging module uses a single logger for the whole file
TESTLOG = 'tests/testlog'

class TestApp(unittest.TestCase):

    def test_applogger(self):
        '''Test the AppLoggerclass'''
        applogger.AppLogger(TESTLOG)
        self.assertEqual(True, str(logging.getLogger('applogger')).startswith('<logging.Logger object at'))
        
    def test_checkbackup(self):
        '''Test the CheckBackup class'''
        _logfile = TESTLOG
        applogger.AppLogger(_logfile)
        checkbackups.CheckBackups({'essai': {'path': 'tests/tar_gz_archive_content/essai.tar.gz', 'files_list': 'tests/tar_gz_archive_content/essai-list', 'type': 'archive'}, 'essai2': {'path': 'tests/tar_bz2_archive_content/titi.tar.bz2', 'files_list': 'tests/tar_bz2_archive_content/essai2-list', 'type': 'archive'}})
        _res = open(_logfile).read()
        os.remove(_logfile)
        self.assertEqual(_res, 'WARNING:root:1 file missing in tests/tar_gz_archive_content/essai.tar.gz: \nWARNING:root:essai/dir/titi\n')

    def test_checkhashes_md5(self):
        '''Test the CheckHashes class with MD5'''
        _hashfile = 'tests/corrupted_archives/MD5SUMS'
        _hashtype = 'md5'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/md5-corrupted.tar.gz', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha1(self):
        '''Test the CheckHashes class with SHA1'''
        _hashfile = 'tests/corrupted_archives/SHA1SUMS'
        _hashtype = 'sha1'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha1-corrupted.tar.gz', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha224(self):
        '''Test the CheckHashes class with SHA224'''
        _hashfile = 'tests/corrupted_archives/SHA224SUMS'
        _hashtype = 'sha224'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha224-corrupted.tar.bz2', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha256(self):
        '''Test the CheckHashes class with SHA256'''
        _hashfile = 'tests/corrupted_archives/SHA256SUMS'
        _hashtype = 'sha256'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha256-corrupted.tar.gz', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha384(self):
        '''Test the CheckHashes class with SHA384'''
        _hashfile = 'tests/corrupted_archives/SHA384SUMS'
        _hashtype = 'sha384'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha384-corrupted.tar.bz2', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checkhashes_sha512(self):
        '''Test the CheckHashes class with SHA512'''
        _hashfile = 'tests/corrupted_archives/SHA512SUMS'
        _hashtype = 'sha512'
        _confs = {'corrupted': {'path': 'tests/corrupted_archives/sha512-corrupted.tar.gz', 'type': 'archive'}}
        __checker = checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        self.assertEqual(0, len(__checker.confs))

    def test_checktar_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        _missingfiles = []
        _missingfiles = checktar.CheckTar({'path':
            'tests/tar_gz_archive_content/essai.tar.gz',
             'files_list':
                'tests/tar_gz_archive_content/essai-list',
             'type': 'archive'}).missing_files
        self.assertEqual(_missingfiles, ['essai/dir/titi'])

    def test_checktar_missing_equality(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'essai/dir/toto')

    def test_checktar_missing_bigger_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'essai/titi')

    def test_checktar_missing_smaller_than(self):
        '''Check if the CheckTar class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'essai/dir/toutou')

    def test_checktree_missing_files(self):
        '''Check if the CheckTar class returns a missing file'''
        __missing_files = []
        __missing_files = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_files
        self.assertEqual(__missing_files, ['foo/bar/toto'])

    def test_checktree_missing_equality(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality= []
        __missing_equality = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'foo/foo1')

    def test_checktree_missing_bigger_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than = []
        __missing_bigger_than = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'foo/foo2')

    def test_checktree_missing_smaller_than(self):
        '''Check if the CheckTree class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than = []
        __missing_smaller_than = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'foo/bar/foo3')

    def test_checkzip_missing_files(self):
        '''Check if the CheckZip class returns a missing file'''
        _missing_files = []
        _missing_files = checkzip.CheckZip({'path':
            'tests/zip/myzip.zip',
             'files_list':
                'tests/zip/myzip-list',
             'type': 'archive'}).missing_files
        self.assertEqual(_missing_files, ['toto/bling'])

    def test_checkzip_missing_equality(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been equal with the expected size'''
        __missing_equality = []
        __missing_equality = checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'myzip/titi')

    def test_checkzip_missing_bigger_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been bigger than the expected size'''
        __missing_bigger_than= []
        __missing_bigger_than = checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'myzip/foo/toto')

    def test_checkzip_missing_smaller_than(self):
        '''Check if the CheckZip class returns a dictionary with a file whose size should have been smaller than the expected size'''
        __missing_smaller_than= []
        __missing_smaller_than = checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'myzip/toutou')

    def test_configurations(self):
        '''Test the Configurations class'''
        __path = 'tests/test_conf/'
        __res = configurations.Configurations(__path).configs
        self.assertEqual({'essai': {'path': 'tests/essai.tar.gz', 'files_list': 'tests/essai-list', 'type': 'archive', 'dbobjects': None, 'dbname': None, 'dbpath': None, 'dbhost': None, 'dbpass': None, 'dbuser': None, 'dbtype': None}}, __res)

    def test_expected_files(self):
        '''Check the ExpectedFiles class'''
        __data = ExpectedFiles('tests/file_size/essai-list').data
        self.assertEqual([{'path':'essai/dir/toto', 'equals':536870912},
            {'path':'essai/titi','biggerthan':536870912},
            {'path':'essai/dir/toutou','smallerthan':20480},
            {'path':'essai/dir/zozo'}], __data)

    def test_unexpected_files(self):
        '''Check if an unexpected file is identified'''
        __data = ExpectedFiles('tests/unexpected_files/files-list').data
        self.assertEqual([{'path':'foo/foo1'},{'path':'foo/foo2'},
            {'path':'foo/bar','unexpected':True}], __data)

    def test_extract_expected_uid_gid(self):
        '''Check the uid and gid of an expected file''' 
        __data = ExpectedFiles('tests/expected_uid_gid/files-list').data
        self.assertEqual([{'path':'foo/foo1', 'uid':1001, 'gid':1001}], __data)

    def test_compare_uid_gid(self):
        '''Compare the uid and the gid of a file in the archive
        and the expected one
        '''
        __uids = []
        __gids = []
        __myobj = checktar.CheckTar({'path':
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
        __data = ExpectedFiles('tests/expected_mode/files-list').data
        self.assertEqual([{'path':'foos/foo1', 'mode': '644'},
            {'path':'foos/foo2', 'mode': '755'},
            {'path':'foos/bar/foo3', 'mode': '4644'},
            {'path':'foos/bar', 'mode': '754'}], __data)

    def test_archive_compare_mode(self):
        '''Compare the mode of a file in the archive and the
        expected one
        '''
        __myobj = checktar.CheckTar({'path':
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
        __myobj = checktree.CheckTree({'path':
            'tests/expected_mode/foo',
             'files_list':
                'tests/expected_mode/treefiles-list',
             'type': 'tree'})
        __modes = __myobj.mismatched_modes
        self.assertEqual(__modes, [
        {'path':'foo/foo1','expectedmode':'664','mode':'644'},
        {'path':'foo/bar','expectedmode':'754','mode':'755'}])

    def test_extract_types(self):
        '''Extract the expected file types'''
        __data = ExpectedFiles('tests/expected_type/files-list').data
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
        __myobj = checktar.CheckTar({'path':
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

    def test_filetree_compare_type(self):
        '''Compare the type of a file in the filetree and the
        expected one
        '''
        __myobj = checktree.CheckTree({'path':
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
        __data = ExpectedFiles('tests/expected_hash/files-list').data
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
        __myobj = checktar.CheckTar({'path':
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

    def test_filetree_compare_hash(self):
        '''Compare the hash of a file in the file tree and the
        expected one
        '''
        __myobj = checktree.CheckTree({'path':
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
        __myobj = checkzip.CheckZip({'path':
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

if __name__ == '__main__':
    unittest.main()
