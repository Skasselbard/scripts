#!/bin/python3

import os
import shutil
import pathlib
import sys


def script_path():
    """path to the current sub script"""
    return os.path.dirname(os.path.abspath(__file__)) + "/"


def main_script_path():
    """ path to the initial called script (with the __main__ context)

        uses the current working dir -> breaks if it was changed
    """
    return os.path.dirname(os.path.abspath(os.getcwd()+'/'+sys.argv[0])) + "/"


def cp(source, dest):
    source = expand_home(source)
    dest = expand_home(dest)
    pathlib.Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)
    shutil.copy(source, dest)


def home():
    return str(pathlib.Path.home())+'/'


def expand_home(path):
    return path.replace('~/', home())
