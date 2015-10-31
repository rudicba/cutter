#!/usr/bin/env python

import magic
import os
import re
import shutil
import subprocess


class Cutter(object):

    def __init__(self):
        self.structure = {}

    def add_file(self, path):
        '''Given a path add to structure'''
        assert os.path.exists(path)

        mime = magic.from_file(path, mime=True)
        self.structure.setdefault(mime, set([])).add(path)

        if mime.decode("utf-8") == 'inode/symlink':
            self.add_file(os.path.realpath(path))
        if mime.decode("utf-8") == 'application/x-executable':
            for librarie in self.ldd(path):
                self.add_file(librarie)

        return True

    def add_folder(self, path):
        for root, dirnames, filenames in os.walk(path):
            for files in filenames:
                file_path = os.path.join(root, files)
                self.add_file(file_path)
        return True

    def add_path(self, path):
        assert os.path.exists(path)

        if os.path.isfile(path):
            self.add_file(path)
        else:
            self.add_folder(path)

    def get_paths(self):
        paths = []
        for mime in self.structure:
            for path in self.structure[mime]:
                paths.append(path)

        return paths

    def ldd(self, path):
        ''' List Dynamic Dependencies '''
        ldd_out = subprocess.check_output(['ldd', str(path)])

        libraries = []
        for line in ldd_out.splitlines():
            match = re.match(r'\t(.*) => (.*) \(0x', line.decode("utf-8"))
            if match:
                libraries.append(match.group(2))
            else:
                # TODO: THIS SUCKS
                libraries.append(line.split()[0].decode("utf-8"))

        # TODO: THIS SUCKS
        libraries.remove('')

        return libraries


def copy_files(filenames):
    for files in filenames:
        rel_path = os.path.relpath(files, '/')
        dst_path = os.path.join('build', rel_path)

        if not os.path.exists(os.path.dirname(dst_path)):
            os.makedirs(os.path.dirname(dst_path))

        shutil.copy2(files, dst_path)
