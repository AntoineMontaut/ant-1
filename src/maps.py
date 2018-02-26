"""maps stuff"""

import json
import os

def load_level_file(level_number):
    """
    read and return a map file's content
    contents are stored as json data
    """

    cwd = os.path.dirname(os.path.abspath(__file__))
    level_file = '{}.json'.format(level_number)
    level_path = os.path.join(cwd, os.pardir, 'levels', level_file)
    with open(level_path, 'r') as f:
        return json.load(f)