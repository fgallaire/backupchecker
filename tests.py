#!/usr/bin/python3

import os
import logging
import sys
import unittest

import brebislogger
import checktar
import checkbackups
import cliparse
import configurations
import expectedfiles
import main

# !! logging module uses a single logger for the whole file
TESTLOG = 'tests/testlog'

class TestBrebis(unittest.TestCase):

    def test_brebislogger(self):
        """Test the Brebis logger"""
        brebislogger.BrebisLogger(TESTLOG)
        self.assertEqual(True, str(logging.getLogger('brebislogger')).startswith('<logging.Logger object at'))
        
    def test_checktar(self):
        """Test the CheckTar class"""
        _missingfiles = []
        _missingfiles = checktar.CheckTar({'path':
            'tests/essai.tar.gz',
             'files_list':
                'tests/essai-list',
             'type': 'archive'}).missing_files
        self.assertEqual(_missingfiles, ['essai/dir/titi'])

    def test_checkbackup(self):
        """Test the CheckBackup class"""
        _logfile = TESTLOG
        brebislogger.BrebisLogger(_logfile)
        checkbackups.CheckBackups({'essai': {'path': 'tests/essai.tar.gz', 'files_list': 'tests/essai-list', 'type': 'archive'}, 'essai2': {'path': 'tests/titi.tar.bz2', 'files_list': 'tests/essai2-list', 'type': 'archive'}})
        _res = open(_logfile).read()
        os.remove(_logfile)
        self.assertEqual(_res, 'INFO:root:1 file missing in tests/essai.tar.gz: \nINFO:root:essai/dir/titi\n')

#    def test_cliparse(self):
#        """Test the CliParse class"""
#        sys.argv = ['./brebis', '-c', 'tests', '-l', 'a.out']
#        self.assertEqual(cliparse.CliParse().options, {'logfile': 'a.out', 'type': None, 'filename': None, 'md5': None, 'confpath': 'tests'})

    def test_configurations(self):
        """Test the Configurations class"""
        _path = 'tests/test_conf/'
        _res = configurations.Configurations(_path).configs
        self.assertEqual({'essai': {'path': 'essai.tar.gz', 'files_list': 'essai-list', 'type': 'archive'}}, _res)

    def test_expectedfiles(self):
        """Test the ExpectedFiles class"""
        _res = []
        _paths = 'tests/essai-list'
        _res = expectedfiles.ExpectedFiles(_paths).paths
        self.assertEqual([_file.rstrip() for _file in open(_paths, 'r').readlines()], _res)

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

