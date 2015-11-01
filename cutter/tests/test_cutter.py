import unittest

from lib import Cutter


class TestCutterLibrary(unittest.TestCase):

    def setUp(self):
        self.cutter = Cutter()
        self.cutter_ls = {
            '/bin/ls', '/lib/x86_64-linux-gnu/libc.so.6', '/lib/x86_64-linux-gnu/ld-2.19.so',
            '/lib/x86_64-linux-gnu/libselinux.so.1', '/lib/x86_64-linux-gnu/libattr.so.1.1.0',
            '/lib/x86_64-linux-gnu/libacl.so.1.1.0', '/lib/x86_64-linux-gnu/libacl.so.1',
            '/lib/x86_64-linux-gnu/libpcre.so.3.13.1', '/lib/x86_64-linux-gnu/libdl.so.2',
            '/lib/x86_64-linux-gnu/libattr.so.1', '/lib64/ld-linux-x86-64.so.2',
            '/lib/x86_64-linux-gnu/libdl-2.19.so', '/lib/x86_64-linux-gnu/libc-2.19.so',
            '/lib/x86_64-linux-gnu/libpcre.so.3'
            }
        self.ldd_ls = [
            '/lib/x86_64-linux-gnu/libselinux.so.1', '/lib/x86_64-linux-gnu/libacl.so.1',
            '/lib/x86_64-linux-gnu/libc.so.6', '/lib/x86_64-linux-gnu/libpcre.so.3',
            '/lib/x86_64-linux-gnu/libdl.so.2', '/lib64/ld-linux-x86-64.so.2',
            '/lib/x86_64-linux-gnu/libattr.so.1'
            ]

    def test_file_are_unique(self):
        self.cutter.add_file('/bin/ls')
        self.cutter.add_file('/bin/ls')
        self.assertEquals(self.cutter.fileset, self.cutter_ls)

    def test_ldd_return_dynamic_dependencies(self):
        ldd = self.cutter.ldd('/bin/ls')
        self.assertEquals(ldd, self.ldd_ls)


if __name__ == '__main__':
    unittest.main()
