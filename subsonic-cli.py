#!/usr/bin/python2

from ConfigParser import RawConfigParser
import os

from pysonic.cli import PySubCli


def main():
    user_config = RawConfigParser()
    user_config.read("%s/.pysonicrc" % (os.path.expanduser('~')))

    config = {}

    for name in user_config.options('general'):
        config[name] = user_config.get('general', name)

    psc = PySubCli(backend=user_config.get('playback', 'backend'), **config)


if __name__ == "__main__":
    main()
