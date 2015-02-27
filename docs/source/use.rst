Use Backup Checker
==================
Two uses of Backup Checker are available:

* generate a description of what's inside the archive
* scan the content of an archive to compare with the associated description

Generate a list of files within a backup
----------------------------------------
Generate the configuration files and the list of files inside for a given archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Starting from 0.4, Backup Checker is able to generate the configuration of a backup and the associated list of files within this backup.

Use the following command to generate the list of files::

    $ backupchecker -G mybackup.tar.gz
    $ ls
    mybackup.tar.gz mybackup.list mybackup.conf

* **mybackup.conf** is the configuration file associated to your archive. See *Configure Backup Checker* section for more details.
* **mybackup.list** is the list of files inside your archive. See *Configure Backup Checker* section for more details.

Generate the configuration files through SSH for a remote archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    $ ssh -q server "cat /tmp/backup.tar.gz" | ./backupchecker -G -

Again, don't forget the last - character in order to trigger the stream mode. By the very nature of the Unix stream, some options are not available using the stream mode. The most annoying one is the feature allowing to compute the hash sums of files inside an archive.

While generating, compute the hash sums of all files in the archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Backup Checker is able to compute the hash sums of all files inside an archive. That was the default from the start of the project to the version 0.9. Given the fact this behaviour heavily loads the computer backupchecker runs on and that the final list of files is protected by a sha512 hash sum written in the associated configuration file (e.g yourbackup.conf), it is safe to make this behaviour optional starting from the version 0.10. The associated options is ``--hashes`` or ``-H``::

    $ backupchecker --hashes -G mybackup.tar.gz
    $ # or
    $ backupchecker -H -G mybackup.tar.gz

Specify that backupchecker need to compute the hash sums of some files inside the archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Backup Checker starting from the version 0.10 by default does not compute any more the hash sum of every files inside an archive except if you use the ``--hashes`` option (heavy compute time for big archives). But you can specify to compute the hash sums of some files - either using the path or a glob syntax - in a list of files you provide thanks to the ``--exceptions-file`` option::

    $ cat archive-exceptions.list
    [files]
    archive/foo| sha1
    archive/bar/*.txt| sha256
    $ backupchecker --exceptions-file archive-exceptions.list -G archive.tar.gz

The result of this command will be two files : the usual configuration file and the list of files inside the archive where only archive/foo and archive/bar/\*.txt will have a hash sum.

Switch the delimiter of fields in the list of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can also modifiy the default delimiter ('|') that backupchecker uses and specify your own with the ``-d`` or ``--delimiter`` option::

    $ backupchecker -d @ -G myarchive.tar.bz
    $ # or
    $ backupchecker  --delimiter @ -c myconfs/myconf.conf

We use @ as the default delimiter for the two commands just above.

Specify the names of configuration files 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, while generating the configuration files of an archive, the names of the generated files are given from the name of the archive. If you need to change these name, use the ``--configuration-name`` option::

    $ backupchecker --configuration-name backup -G archive.tar.gz
    $ ls *.conf *.list
    $ backup.conf backup.list 


Scan the content of an archive to compare with the associated description
-------------------------------------------------------------------------
Common use case
^^^^^^^^^^^^^^^
You launch the scan mode of Backup Checker from the command line with the following command::

   $ backupchecker -c myconfs/

The option ``-c`` or ``--configpath`` specifies a path to a directory where your Backup Checker configurations are stored. If any alert is triggered, it will appear in the your current working directory in a file named a.out. Relative or absolute paths are accepted.

You can also specify your own output file::

   $ backupchecker -c myconfs/ -l output/backupchecker.log

The option ``-l`` or ``--log`` specifies your own output file.

Verify a remote archive
^^^^^^^^^^^^^^^^^^^^^^^
Verify an archive on a remote server from a FTP server::

    $ wget --quiet -O - ftp://user:pass@server/backup.tar.gz | ./backupchecker -c /path/to/conf/dir -

Don't forget the last - character, triggering the stream mode of Backup Checker.

Change the path to the configuration file and the list of files for a given archive

By default, the files containing the different parameters of the content of the archive and the configuration file are created in the same directory as the archive itself. From Backup Checker 0.9, you can specifiy a custom directory for the configuration file (the ``-C`` option), for the list of files (the ``-L`` option) or both with the ``-O`` option::

    $ backupchecker -c /etc/backupchecker/ -l /var/log/backupchecker.log -C /etc/backupchecker/confs/ -L /etc/backupchecker/lists/

The example above indicates a /etc/backupchecker/confs directory to store the configuration files of Backup Checker and a /etc/backupchecker/lists/ directory to store the list of files of Backup Checker.
