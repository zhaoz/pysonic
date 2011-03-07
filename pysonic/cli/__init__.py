"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

from optparse import OptionParser
import re
import readline
import shlex
import sys

from pysonic import pretty
from pysonic.api import Subsonic
from pysonic.player import SubPlayer
from pysonic.cli.search import Search


class PySubCli(object):

    def __init__(self, username=None, password=None, server=None, backend="mad"):
        self.api = Subsonic(username=username, password=password,
                server=server)

        self.player = SubPlayer(subsonic=self.api, playend=backend)
        self.search = Search(self.api)

        self.cur_list = None

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

        self.cur_list = self.getList(search_by, options)
        print self.cur_list

    def getList(self, field, options):
        if field == 'artist':
            return self.search.search_artist(options)
        elif field == 'song':
            return self.search.search_song(options)

    def dump(self, args):
        """Dump json representation."""
        if not self.cur_list:
            print "No list to operate on."
            return

        if len(args) < 1:
            print repr(self.cur_list)
            return

        try:
            num = int(args[0])
            print pretty(self.cur_list[num])
        except ValueError, ex:
            print "Wrong format"

    def play(self, args):
        """Play something."""

        try:
            num = int(args[0]) - 1
            self.player.play(self.cur_list[num])
            return
        except IndexError, ex:
            print "That's not in the list."
            return
        except ValueError, ex:
            # don't care about this
            pass

        # maybe its an ID?
        id_re = re.compile(r'^[a-f0-9]+$')

        if id_re.match(args[0]):
            self.player.play(song_id=args[0])


    def execArgs(self, args):
        """Execute commands given on the cli."""
        cmd = args[0]

        if cmd == 'search':
            self.searchArgs(args[1:])
        elif cmd == 'relist':
            print self.cur_list
        elif cmd == 'dump':
            self.dump(args[1:])
        elif cmd == 'play':
            self.play(args[1:])

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

