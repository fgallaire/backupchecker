### BackupChecker 

BackupChecker is an automated backup checker. Read the documentation in docs/
or [read it online](https://backupchecker.readthedocs.org/en/latest/).

### Quick Start

* Install Backup Checker from PyPI

        # pip install backupchecker

* Install Backup Checker from sources

        # tar zxvf backupchecker-1.1.tar.gz
        # cd backupchecker
        # python3.4 setup.py install
        # # or
        # python3.4 setup.py install --install-scripts=/usr/bin

* Generate the configuration files for a given archive:

        $ backupchecker  -G /path/to/backup.tar.gz

* Verify the archive and its content:

        $ backupchecker -c /path/to/confs/

### Authors

Carl Chenet <chaica@backupchecker.com>

### License

This software comes under the terms of the GPLv3+. See the LICENSE file for the complete text of the license.
