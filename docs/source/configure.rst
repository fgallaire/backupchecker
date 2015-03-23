Configure Backup Checker

You need two files in order to use Backup Checker, a file offering the configuration of the archive and another file giving the detail of what's inside the archive, let's call it the list of files. But don't worry, the option -G allows to generate both files from a given archive. The next sections offer the details of what parameter these files contain.

Configuration of the archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The first one contains general information about the backup checking session. It is mandatory your configuration file uses the .conf extension. Here is an example with all the currently supported parameters::

    [main]
    name=mybackup-checking-session
    type=archive
    path=tests/expected_mode/foos.tar.gz
    files_list=tests/expected_mode/files-list
    delimiter=|
    sha512=87d3325d3bb844734c1b011fb0f12a3ae47676153a8b05102a5e1b5347a86096d85b1b239752c3fdc10a8a2226928b64b5f31d8fd09f3e43a8eee3a4228f38b1

* **[main]** is mandatory.
* **name** is the name of your backup checking session. If you have several backup checking sessions, they MUST use a different name.
* **type** is the type of your backup. Currently you only have archive (tar, tar.gz, tar.bz2, zip files) and tree for a tree of directories and files.
* **path** is the path to the archive or the top directory of your files tree. Relative or absolute paths are accepted.
* **files_list** is the path to the file containing the information about the archive, the tree or the files inside your backups. Relative or absolute paths are accepted.
* **delimiter** (optional field) is the string to use in the list of files to mark the end of the key and the beginning of the value. Default is | (pipe).
* **sha512** (optional field) provides the sha512 hash sum of the list of files, in order to check if this file is the expected one.

Understanding the parameters of the list of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The second file you need is the list containing the information about the archive, the tree or the files inside your backups. Here is an example with the full list of the parameters available for now::

    [archive]
    size| <5m
    mode| 755
    uid| 5000
    gid| 5001
    owner| chaica
    group| sysadmin
    sha1| e0f58dcc57caad2182f701eb63f0c81f347d3fe5
    mtime| 1425890843.0
    outdated| 2 months
    
    [files]
    foos/foo|
    foos/foo1| >105k type|f mode|755 uid|5022 gid|5023 owner|chaica group|sysadmin unexpected md5|3718422a0bf93f7fc46cff6b5e660ff8

* **[archive]** section hosts the parameter for the archive itself. This section is not mandatory if you do not need it.
* **size** defines what the archive size should be. You can specify <,> or =. Default value is expressed in bytes, also available are (k)ilo, (m)ega, (g)iga, (p)eta,(e)xa, (z)etta and (y)ottabyte.
* **mode** is for the expected mode of the archive.
* **uid** is for the expected uid of the archive.
* **gid** is for the expected gid of the archive.
* **owner** is the name of the owner of this file in the archive.
* **group** is the name of the owner group of this file in the archive.
* **sha1** is for the expected md5 hash sum of the archive. Also available is sha1, sha224, sha256, sha384, sha512.
* **mtime** it is the posix timestamp of the last modification of the archive. It is usually automatically generated.
* **outdated** takes a duration starting from the mtime of the archive. Afther this duration, a warning is triggered to warn that the archive is outdated.

* **[files]** section stands for the files inside the archive or the tree of directories and files. This section is not mandatory if you do not need it.
* **foos/foo|** means this file has to exist in the backup, whatever it is.
* **foos/foo1| >105k** defines that the file size of foos/foo1 in the archive should be strictly bigger than 105 kilobytes. You can specify <,> or =. Default value is expressed in bytes, also available are (k)ilo, (m)ega, (g)iga, (p)eta,(e)xa, (z)etta and (y)ottabyte.
* **foos/foo1| type|f** means the file foos/foo1 is expected to be of type f. Several types are allowed : f for files, d for directory, s for symbolic link, k for socket, b for block, c for character.
* **foos/foo1| mode|755** means the file foos/foo1 is expected to have the mode 755 (meaning read, write and execute for the owner, read and execute for the group owner, read and execute for the others). All values respecting this octal representation (including values with setuid bit on four digits) is allowed.
* **foos/foo1| uid|5022** means the file foos/foo1 is expected to have a uid of 5022.
* **foos/foo1| gid|5023** means the file foos/foo1 is expected to have a gid of 5023.
* **foos/foo1| owner|chaica** means the file foos/foo1 is expected to be owned by the user with the name chaica.
* **foos/foo1| group|sysadmin** means the file foos/foo1 is expected to be owned by the owner group with the name sysadmin.
* **foo/bar| unexpected** means that foo/bar is unexpected in this archive of tree of directories and files and that an alert should be launched about it.
* **foos/foo1| md5|hashsum** means the file foos/foo1 is expected to have a md5 hash sum of "hashsum". Also available is sha1, sha224, sha256, sha384, sha512.
