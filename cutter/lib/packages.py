import apt
import os
import subprocess
import requests


class Package(object):
    """
    """
    def __init__(self):
        self.installed = []
        self.downloaded = []
        self.dependencies = []

        self.download_folder = '/tmp/.cuttercache'

        self.cache = apt.Cache()

        if not os.path.isdir(self.download_folder):
            os.makedirs(self.download_folder)

    def get_dependencies(self, pkg_name):
        pkg = self.cache[pkg_name]

        if pkg_name not in self.dependencies:
            self.dependencies.append(pkg_name)
            # Search and install all dependencies
            for pkg_dep in pkg.versions[0].dependencies:
                self.get_dependencies(pkg_dep[0].name)

    def _download_destination(self, pkg):
        file_name = os.path.basename(pkg.versions[0].filename)
        return os.path.join(self.download_folder, file_name)

    def download_package(self, pkg):
        destination = self._download_destination(pkg)

        # TODO Don't re-download
        if os.path.isfile(destination):
            return False

        # TODO Check response.ok
        response = requests.get(pkg.versions[0].uri, stream=True)

        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Filter out keep-alive new chunks
                    f.write(chunk)

        return True

    def install_with_dependencies(self, pkg_name):
        self.get_dependencies(pkg_name)

        for package in self.dependencies:
            self.install_package(package)

    def install_package(self, pkg_name):
        pkg = self.cache[pkg_name]

        if pkg_name not in self.downloaded:
            if self.download_package(pkg):
                self.downloaded.append(pkg_name)

        print("Installing %s from %s" % (pkg_name, self._download_destination(pkg)))
        subprocess.check_call(['ar', 'x', self._download_destination(pkg)])
        self.installed.append(pkg_name)

        return False
