#!/bin/bash
#
# This script converts brebis to backupchecker
#

# Rename files from brebis to backupchecker
mv -f ./brebis ./backupchecker
mv -f ./brebis.py ./backupchecker.py
mv -f ./scripts/brebis ./scripts/backupchecker 
rm -rf ./__pycache__

# Modify information in ./setup.py
sed -i 's/brebisproject.org/backupchecker.com/g' ./setup.py
sed -i 's/chaica/carl.chenet/g' ./setup.py
sed -i 's/Brebis/BackupChecker/g' ./setup.py

# Rename all occurrences of brebis in backupchecker
find . -type f -iname "*.py" -print| xargs /bin/sed -i 's/brebis/backupchecker/g'
