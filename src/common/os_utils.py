from pathlib import Path
import os


def get_root_folder():
    """ return the absolute path of our main project """
    return Path(os.path.dirname(os.path.abspath(__file__))).parent
