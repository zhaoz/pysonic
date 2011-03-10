#!/usr/bin/python2

import sys

import pysonic
from pysonic.cli import PySubCli


def main():

    cfg = pysonic.ReadConfig()

    psc = PySubCli(config=cfg)

    if len(sys.argv) < 2:
        print "Need to give at least one arg"
        sys.exit(1)

    args = sys.argv[1:]

    if args[0] == 'shell':
        psc.shell()
    else:
        psc.execArgs(args)


if __name__ == "__main__":
    main()
