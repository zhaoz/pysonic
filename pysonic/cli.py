"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

from optparse import OptionParser
import sys

import simplejson

from pysonic.api import Subsonic
from pysonic.player import SubPlayer


def prettyPrint(json):
    print simplejson.dumps(json, sort_keys=True, indent=4 * ' ')


def makeArray(obj):
    if type(obj) is not list:
        return [obj,]
    return obj


class PySubCli(object):

    def __init__(self, username=None, password=None, server=None, backend="mad"):
        self.api = Subsonic(username=username, password=password,
                server=server)

        self.parseArgs(sys.argv[1:])

        self.player = SubPlayer(subsonic=self.api, playend=backend)

    def search(self, args):
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

        if search_by == 'artist':
            self.search_artist(options)
        elif search_by == 'song':
            self.search_song(options)

    def search_song(self, options):
        query = {
                'query': options.song
                }

        result = self.api.call_search2(query=query)
        songs = makeArray(result['searchResult2']['song'])

        cnt = 0
        for song in songs:
            cnt += 1
            print "%d. %s - %s - %s - %s" % (cnt, song['album'],
                    song['track'], song['artist'], song['title'])


    def search_artist(self, options):
        query = {
                'query': options.artist
                }
        result = self.api.call_search2(query=query)

        artists = makeArray(result['searchResult2']['artist'])

        cnt = 0
        for artist in artists:
            cnt += 1
            print "%d. %s" % (cnt, artist['name'])


    def parseArgs(self, args):
        if args[0] == 'search':
            self.search(args[1:])

