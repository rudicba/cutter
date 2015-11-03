import configparser
import os
import shutil
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
    destination = config.get('Global', 'destination')

    cutter = Cutter()

    for project in project_list:
        for path in config.get(project, 'Paths').split():
            cutter.add_path(path)

    for file_path in cutter.fileset:
        # Remove root from file_path
        dst_path = os.path.join(destination, os.path.relpath(file_path, '/'))
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(file_path, dst_path)
        print('Copying: %s to %s' % (file_path, dst_path))
