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

# Replace brebis by backupchecker in ./generate-archive.sh
sed -i 's/brebis/backupchecker/g' ./generate-archive.sh

# Replace brebis by backupchecker in ./AUTHORS
sed -i 's/brebisproject.org/backupchecker.com/g' ./AUTHORS

# Replace brebis, Brebis and brebisproject.org in ./README
sed -i 's/brebisproject.org/backupchecker.com/g' ./README
sed -i 's/Brebis/BackupChecker/g' ./README
sed -i 's/brebis/backupchecker/g' ./README

# Replace brebis, Brebis and brebisproject.org in ./README
sed -i 's/Brebis/BackupChecker/g' ./changelog
sed -i 's/brebis/backupchecker/g' ./changelog

# rename ./man/brebis.1 to ./man/backupchecker.1
mv -f ./man/brebis.1 ./man/backupchecker.1
# Replace BREBIS, Brebis, brebis, brebisproject.org in ./man/brebis.1
sed -i 's/chaica/carl.chenet/g' ./man/backupchecker.1
sed -i 's/brebisproject.org/backupchecker.com/g' ./man/backupchecker.1
sed -i 's|brebisproject\\&\.org|backupchecker\\\&.com|g' ./man/backupchecker.1
sed -i 's/BREBIS/BACKUPCHECKER/g' ./man/backupchecker.1
sed -i 's/brebis/backupchecker/g' ./man/backupchecker.1
sed -i 's/Brebis/BackupChecker/g' ./man/backupchecker.1

# Rename all occurrences of brebis in backupchecker
find . -type f -iname "*.py" -print| xargs /bin/sed -i 's/brebis/backupchecker/g'
