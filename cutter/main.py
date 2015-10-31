import configparser
import sys

from lib import Cutter
from lib import Options

if __name__ == '__main__':
    options = Options()
    opts = options.parse(sys.argv[1:])

    config = configparser.ConfigParser()
    config.read(opts.config)

    # Get all projects from config
    project_list = [p for p in config.sections() if p != 'Global']

    cutter = Cutter()

    for project in project_list:
        for path in config.get(project, 'Paths').split():
            cutter.add_path(path)

    print(cutter.get_paths())
