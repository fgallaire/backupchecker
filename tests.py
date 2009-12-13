#!/usr/bin/python3

import os
import logging
import sys
import unittest

import brebislogger
import checkbackups
import checkhashes
import checktar
import checktree
import checkzip
import cliparse
import configurations
import expectedfiles
import main

# !! logging module uses a single logger for the whole file
TESTLOG = 'tests/testlog'

class TestBrebis(unittest.TestCase):

    def test_brebislogger(self):
        """Test the BrebisLogger class"""
        brebislogger.BrebisLogger(TESTLOG)
        self.assertEqual(True, str(logging.getLogger('brebislogger')).startswith('<logging.Logger object at'))
        
    def test_checkbackup(self):
        """Test the CheckBackup class"""
        _logfile = TESTLOG
        brebislogger.BrebisLogger(_logfile)
        checkbackups.CheckBackups({'essai': {'path': 'tests/essai.tar.gz', 'files_list': 'tests/essai-list', 'type': 'archive'}, 'essai2': {'path': 'tests/titi.tar.bz2', 'files_list': 'tests/essai2-list', 'type': 'archive'}})
        _res = open(_logfile).read()
        os.remove(_logfile)
        self.assertEqual(_res, 'WARNING:root:1 file missing in tests/essai.tar.gz: \nWARNING:root:essai/dir/titi\n')

    def test_checkhashes(self):
        """Test the CheckHashes class"""
        _hashfile = 'tests/corrupted_archive/MD5SUMS'
        _hashtype = 'md5'
        _confs = {'essai': {'path': '/home/chaica/progra/python/brebis/tests/corrupted_archive/essai.tar.gz', 'files_list': '/home/chaica/progra/python/brebis/tests/corrupted_archive/essai-list', 'type': 'archive'}, 'corrupted': {'path': '/home/chaica/progra/python/brebis/tests/corrupted_archive/corrupted.tar.gz', 'files_list': '/home/chaica/progra/python/brebis/tests/corrupted_archive/essai-list', 'type': 'archive'}}
        checkhashes.CheckHashes(_hashfile, _hashtype, _confs)
        _res = open('tests/corrupted_archive/a.out').read()
        self.assertEqual(_res, 'INFO:root:The /home/chaica/progra/python/brebis/tests/corrupted_archive/corrupted.tar.gz checksum mismatched\nINFO:root:1 file missing in /home/chaica/progra/python/brebis/tests/corrupted_archive/essai.tar.gz: \nINFO:root:essai/dir/titi\n')

    def test_checktar_missing_files(self):
        """Check if the CheckTar class returns a missing file"""
        _missingfiles = []
        _missingfiles = checktar.CheckTar({'path':
            'tests/essai.tar.gz',
             'files_list':
                'tests/essai-list',
             'type': 'archive'}).missing_files
        self.assertEqual(_missingfiles, ['essai/dir/titi'])

    def test_checktar_missing_equality(self):
        """Check if the CheckTar class returns a dictionary with a file whose size should have been equal with the expected size"""
        __missing_equality = []
        __missing_equality = checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'essai/dir/toto')

    def test_checktar_missing_bigger_than(self):
        """Check if the CheckTar class returns a dictionary with a file whose size should have been bigger than the expected size"""
        __missing_bigger_than = []
        __missing_bigger_than = checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'essai/titi')

    def test_checktar_missing_smaller_than(self):
        """Check if the CheckTar class returns a dictionary with a file whose size should have been smaller than the expected size"""
        __missing_smaller_than = []
        __missing_smaller_than = checktar.CheckTar({'path':
            'tests/file_size/essai.tar.bz2',
             'files_list':
                'tests/file_size/essai-list',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'essai/dir/toutou')

    def test_checktree_missing_files(self):
        """Check if the CheckTar class returns a missing file"""
        __missing_files = []
        __missing_files = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_files
        self.assertEqual(__missing_files, ['foo/bar/toto'])

    def test_checktree_missing_equality(self):
        """Check if the CheckTree class returns a dictionary with a file whose size should have been equal with the expected size"""
        __missing_equality= []
        __missing_equality = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'foo/foo1')

    def test_checktree_missing_bigger_than(self):
        """Check if the CheckTree class returns a dictionary with a file whose size should have been bigger than the expected size"""
        __missing_bigger_than = []
        __missing_bigger_than = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'foo/foo2')

    def test_checktree_missing_smaller_than(self):
        """Check if the CheckTree class returns a dictionary with a file whose size should have been smaller than the expected size"""
        __missing_smaller_than = []
        __missing_smaller_than = checktree.CheckTree({'path':
            'tests/filetree/foo',
             'files_list':
                'tests/filetree/filelist',
             'type': 'tree'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'foo/bar/foo3')

    def test_checkzip_missing_files(self):
        """Check if the CheckZip class returns a missing file"""
        _missing_files = []
        _missing_files = checkzip.CheckZip({'path':
            'tests/myzip.zip',
             'files_list':
                'tests/myzip-list',
             'type': 'archive'}).missing_files
        self.assertEqual(_missing_files, ['toto/bling'])

    def test_checkzip_missing_equality(self):
        """Check if the CheckZip class returns a dictionary with a file whose size should have been equal with the expected size"""
        __missing_equality = []
        __missing_equality = checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_equality
        self.assertEqual(__missing_equality[0]['path'], 'myzip/titi')

    def test_checkzip_missing_bigger_than(self):
        """Check if the CheckZip class returns a dictionary with a file whose size should have been bigger than the expected size"""
        __missing_bigger_than= []
        __missing_bigger_than = checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_bigger_than
        self.assertEqual(__missing_bigger_than[0]['path'], 'myzip/foo/toto')

    def test_checkzip_missing_smaller_than(self):
        """Check if the CheckZip class returns a dictionary with a file whose size should have been smaller than the expected size"""
        __missing_smaller_than= []
        __missing_smaller_than = checkzip.CheckZip({'path':
            'tests/file_size/myzip.zip',
             'files_list':
                'tests/file_size/essai-list2',
             'type': 'archive'}).missing_smaller_than
        self.assertEqual(__missing_smaller_than[0]['path'], 'myzip/toutou')

    def test_configurations(self):
        """Test the Configurations class"""
        __path = 'tests/test_conf/'
        __res = configurations.Configurations(__path).configs
        self.assertEqual({'essai': {'path': 'tests/essai.tar.gz', 'files_list': 'tests/essai-list', 'type': 'archive', 'dbobjects': None, 'dbpath': None, 'dbhost': None, 'dbpass': None, 'dbuser': None, 'dbtype': None}}, __res)

    def test_expectedfiles(self):
        """Test the ExpectedFiles class"""
        _res = []
        _paths = 'tests/essai-list'
        _data = expectedfiles.ExpectedFiles(_paths).data
        self.assertEqual([_file.rstrip() for _file in open(_paths, 'r').readlines()], [_file['path'] for _file in _data])

#    def test_main(self):
#        """Test the Main class"""
#        _output = TESTLOG
#        sys.argv = ['./brebis', '-c', 'tests/', '-l', _output]
#        main.Main()
#        _res = open(_output).read()
#        os.remove(_output)
#        self.assertEqual(_res, 'INFO:root:1 file missing in /home/chaica/progra/python/brebis/tests/essai.tar.gz: \nINFO:root:essai/dir/titi\n')

if __name__ == '__main__':
    unittest.main()
