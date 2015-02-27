Unsupported parameters for a given kind of archive
==================================================
Given the very nature of the different kind of archive formats, some parameters are not supported for a given archive type (e.g for a bzip2 file, original rights and mode of the file inside the archive are not saved). An explicit warning will appear in the backup checker log file if you are using an unsupported feature for a given type of archive.

Unsupported parameters for the remote archive
=============================================
By the nature of Unix streams, some options commonly available while using Backup Checker from a local host are not available from a remote host. The most annoying one is that computing the hash sums of files inside an archive is not possible for a stream.
