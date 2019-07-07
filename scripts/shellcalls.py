#!/bin/python3

from subprocess import run, DEVNULL
from shutil import which
from scripts.paths import home
import os
import sys
import warnings
import pathlib


def get_install_program():
    # adapt this for other distros than ubuntu
    return "sudo apt install -y "


def expand_home(path):
    return path.replace('~/', home())


def install(programs):
    not_installed = ""
    for program in programs.split(' '):
        if is_installed(program):
            print(program + " is already installed")
        else:
            not_installed += program + ' '
    if not_installed != "":
        call(get_install_program() + not_installed)


def is_installed(program):
    return which(program) != None


def call(cmd):
    run(expand_home(cmd).split(' '), check=True)


def raw_call(cmd, surpressOutput=False):
    if surpressOutput:
        run(expand_home(cmd), shell=True, check=True, stdout=DEVNULL)
    else:
        run(expand_home(cmd), shell=True, check=True)


def clone(repo, dest):
    dest = expand_home(dest)
    if not os.path.isdir(dest):
        pathlib.Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)
    if not os.listdir(dest):
        call("git clone " + repo + " " + dest)
    else:
        print("Cannot clone to destination. Directory " +
              dest + " is not empty. Skipping clone")
