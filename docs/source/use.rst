Use Brebis
==========

Two uses of brebis are available:

* generate a description of what's inside the archive
* scan the content of an archive to compare with the associated description

Generate a list of files within a backup
----------------------------------------

Generate the configuration files and the list of files inside for a given archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starting from 0.4, Brebis is able to generate the configuration of a backup and the associated list of files within this backup.

Use the following command to generate the list of files:::

    $ brebis -G mybackup.tar.gz
    $ ls
    mybackup.tar.gz mybackup.list mybackup.conf

* **mybackup.conf** is the configuration file associated to your archive. See *Configure Brebis* section for more details.
* **mybackup.list** is the list of files inside your archive. See *Configure Brebis* section for more details.

While generating, compute the hash sums of all files in the archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Brebis is able to compute the hash sums of all files inside an archive. That was the default from the start of the project to the version 0.9. Given the fact this behaviour heavily loads the computer brebis runs on and that the final list of files is protected by a sha512 hash sum written in the associated configuration file (e.g yourbackup.conf), it is safe to make this behaviour optional starting from the version 0.10. The associated options is ``--hashes`` or -H.::

    $ brebis --hashes -G mybackup.tar.gz
    $ # or
    $ brebis -H -G mybackup.tar.gz

Specify that brebis need to compute the hash sums of some files inside the archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Brebis starting from the version 0.10 by default does not compute any more the hash sum of every files inside an archive except if you use the ``--hashes`` option (heavy compute time for big archives). But you can specify to compute the hash sums of some files - either using the path or a glob syntax - in a list of files you provide thanks to the --exceptions-file option:::

    $ cat archive-exceptions.list
    archive/foo| sha1
    archive/bar/*.txt| sha256
    $ brebis --exceptions-file archive-exceptions.list -G archive.tar.gz

The result of this command will be two files : the usual configuration file and the list of files inside the archive where only archive/foo and archive/bar/\*.txt will have a hash sum.

Switch the delimiter of fields in the list of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also modifiy the default delimiter ('|') that brebis uses and specify your own with the -d or --delimiter option:::

    $ brebis -d @ -G myarchive.tar.bz
    $ # or
    $ brebis  --delimiter @ -c myconfs/myconf.conf

We use @ as the default delimiter for the two commands just above.

Scan the content of an archive to compare with the associated description
-------------------------------------------------------------------------

Common use case
^^^^^^^^^^^^^^^
You launch the scan mode of Brebis from the command line with the following command:::

   $ brebis -c myconfs/

The option -c or ``--configpath`` specifies a path to a directory where your Brebis configurations are stored. If any alert is triggered, it will appear in the your current working directory in a file named a.out. Relative or absolute paths are accepted.

You can also specify your own output file:::

   $ brebis -c myconfs/ -l output/brebis.log

The option -l or ``--log`` specifies your own output file.

Change the path to the configuration file and the list of files for a given archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, the files containing the different parameters of the content of the archive and the configuration file are created in the same directory as the archive itself. From Brebis 0.9, you can specifiy a custom directory for the configuration file (the -C option), for the list of files (the -L option) or both with the -O option.::

    $ brebis -c /etc/brebis/ -l /var/log/brebis.log -C /etc/brebis/confs/ -L /etc/brebis/lists/

The example above indicates a /etc/brebis/confs directory to store the configuration files of Brebis and a /etc/brebis/lists/ directory to store the list of files of Brebis.
