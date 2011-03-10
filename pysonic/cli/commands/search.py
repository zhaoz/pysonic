"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.com>'


from optparse import OptionParser

import pysonic.cli as cli

from pysonic.cli.commands import command
import pysonic.cli.commands.base as base
from pysonic.cli.search import Search

@command
class SearchCommand(base.BaseCommand):
    COMMANDS = ['search']

    def __init__(self):
        self._inited = False

    def _real_init(self, api):
        if self._inited:
            return

        self.api = api
        self.search = Search(self.api)

    def __call__(self, api, args):
        self._real_init(api)

        cmd = args[0]
        self.searchArgs(args[1:])

    def searchArgs(self, args):
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

        lst = self.getList(search_by, options)
        cli.instance.cur_list = lst
        print lst

    def getList(self, field, options):
        if field == 'artist':
            return self.search.search_artist(options)
        elif field == 'song':
            return self.search.search_song(options)

