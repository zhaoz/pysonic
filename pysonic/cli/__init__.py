"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

from optparse import OptionParser
import readline
import shlex
import sys

import simplejson

from pysonic.api import Subsonic
from pysonic.player import SubPlayer
from pysonic.cli.search import Search


def prettyPrint(json):
    print simplejson.dumps(json, sort_keys=True, indent=4 * ' ')


class PySubCli(object):

    def __init__(self, username=None, password=None, server=None, backend="mad"):
        self.api = Subsonic(username=username, password=password,
                server=server)

        self.player = SubPlayer(subsonic=self.api, playend=backend)
        self.search = Search(self.api)

        self.cur_list = None

    def search_args(self, args):
        parser = OptionParser()

        parser.add_option('-a', '--artist', dest='artist')
        parser.add_option('-s', '--song', dest='song')
        parser.add_option('-b', '--album', dest='album')

        search_by = 'song'

        for name in ('artist', 'song'):
            if args[0] == name:
                parser.remove_option('--%s' % name)
                search_by = args.pop(0)
                kwargs = {}
                kwargs[name] = args.pop(0)
                parser.set_defaults(**kwargs)
                break

        (options, args) = parser.parse_args(args=args)

        self.cur_list = self.get_list(search_by, options)
        print self.cur_list

    def get_list(self, field, options):
        if field == 'artist':
            return self.search.search_artist(options)
        elif field == 'song':
            return self.search.search_song(options)

    def execArgs(self, args):
        if args[0] == 'search':
            self.search_args(args[1:])

    def shell(self):
        while True:
            try:
                raw = raw_input(">>> ")
            except EOFError, ex:
                print "\nExiting"
                break
            except KeyboardInterrupt, ex:
                print "\nInteruptted -- Exiting"
                sys.exit(0)

            self.execArgs(shlex.split(raw))

