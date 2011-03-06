#!/usr/bin/python2

import os
from ConfigParser import RawConfigParser

from pysonic.api import Subsonic
from pysonic.player import SubPlayer

def prettyPrint(json):
    print simplejson.dumps(json, sort_keys=True, indent=4 * ' ')

class PySubCli(object):

    def __init__(self, username=None, password=None, server=None, backend="mad"):
        self.api = Subsonic(username=username, password=password,
                server=server)

        self.player = SubPlayer(subsonic=self.api, playend=backend)

def main():
    user_config = RawConfigParser()
    user_config.read("%s/.pysonicrc" % (os.path.expanduser('~')))

    config = {}

    for name in user_config.options('general'):
        config[name] = user_config.get('general', name)

    psc = PySubCli(backend=user_config.get('playback', 'backend'), **config)


if __name__ == "__main__":
    main()
