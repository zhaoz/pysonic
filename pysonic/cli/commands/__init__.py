"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.com>'

import os
import glob


register = {}

def command(cls):
    for cmd in cls.COMMANDS:
        register[cmd] = cls()


def register_all():
    for f in glob.glob(os.path.dirname(__file__) + "/*.py"):
        name = os.path.basename(f)[:-3]

        if name is not "__init__":
            __import__("%s.%s" % (__name__, name))

def find(args):
    cmd = args[0]
    if cmd not in register:
        raise KeyError("Command doesn't exist")
    
    return register[cmd]


