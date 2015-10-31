import unittest

from lib import Options


class TestCommandLineParameters(unittest.TestCase):

    def setUp(self):
        self.options = Options()

    def test_defaults_options_are_set(self):
        opts = self.options.parse()
        self.assertEquals(opts.config, 'config/cutter.ini')

    def test_options_config_is_set(self):
        opts = self.options.parse(['-c', 'config_file'])
        self.assertEquals(opts.config, 'config_file')

        opts = self.options.parse(['--config', 'config_file'])
        self.assertEquals(opts.config, 'config_file')


if __name__ == '__main__':
    unittest.main()
