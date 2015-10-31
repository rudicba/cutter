from argparse import ArgumentParser


class Options(object):

    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'bin/project'
        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument('-c',
                                 '--config',
                                 default='config/cutter.ini',
                                 dest='config',
                                 help='Config file path')

    def parse(self, args=None):
        return self.parser.parse_args(args)
