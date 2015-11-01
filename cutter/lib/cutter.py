#!/usr/bin/env python

import magic
import os
import re
import subprocess


class Cutter(object):
    """Handle file dependencies

    Note:
        Cutter will track needed files for running executables inside a chroot environment.

    Attributes:
        fileset (array set): All files needed for project.
        folderset (array set): Folders needed for project.

    Examples:
        >>> cutter = Cutter()
        >>> cutter.add_file('/bin/ls')
        >>> cutter.fileset
        {'/bin/ls',
         '/lib/x86_64-linux-gnu/ld-2.19.so',
         '/lib/x86_64-linux-gnu/libacl.so.1',
         ......
         '/lib64/ld-linux-x86-64.so.2'}
         >>> cutter.folderset
         {'/bin', '/lib/x86_64-linux-gnu', '/lib64'}
    """

    def __init__(self):
        self.fileset = set([])
        self.folderset = set([])

    def add_file(self, path):
        """Add file to fileset, update folderset.

        Note:
            If file is symlink add symlink detination to fileset.
            If file is x-executable search for Dynamic Dependencies and recursively add.

        Args:
            path: Path of file to add to fileset.

        Returns:
            True if successful, False otherwise.

        """
        assert os.path.exists(path)

        mime = magic.from_file(path, mime=True)
        self.fileset.add(path)
        self.folderset.add(os.path.dirname(path))

        if mime.decode("utf-8") == 'inode/symlink':
            self.add_file(os.path.realpath(path))
        if mime.decode("utf-8") == 'application/x-executable':
            for librarie in self.ldd(path):
                self.add_file(librarie)

        return True

    def add_folder(self, path):
        """Add path to fileset.

        Note:
            If path is folder add all folder and subfolder files to fileset.
            If path if file add file to fileset.

        Args:
            path: Path of file or folder to add to fileset.

        Returns:
            True if successful, False otherwise.

        """
        assert os.path.isdir(path)

        for root, dirnames, filenames in os.walk(path):
            for files in filenames:
                file_path = os.path.join(root, files)
                self.add_file(file_path)

        return True

    def add_path(self, path):
        """Add path to fileset.

        Args:
            path: Path of folder to walk.

        Returns:
            True if successful, False otherwise.

        """
        assert os.path.exists(path)

        if os.path.isfile(path):
            self.add_file(path)
        else:
            self.add_folder(path)

    def ldd(self, path):
        """List Dynamic Dependencies.

        Args:
            path: Path of x-executable file.

        Returns:
            List of all Dynamic Dependencies needed for executable

        """
        ldd_out = subprocess.check_output(['ldd', str(path)])

        libraries = []
        for line in ldd_out.splitlines():
            match = re.match(r'\t(.*) => (.*) \(0x', line.decode("utf-8"))
            if match:
                libraries.append(str(match.group(2)))
            else:
                # TODO: THIS SUCKS
                libraries.append(str(line.split()[0].decode("utf-8")))

        # TODO: THIS SUCKS
        libraries.remove('')

        return libraries
