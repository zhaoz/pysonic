"""pysonic library.
"""

import re

from pysonic import pretty

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'


def makeArray(obj):
    if type(obj) is not list:
        return [obj,]
    return obj


class Search(object):
    def __init__(self, api):
        self.api = api

    def _getList(self, item, key):
        if type(item) is dict:
            return item[key]

        return []


    def search_song(self, options):
        qs = [options.song,]

        if options.artist:
            qs.append(options.artist)
        if options.album:
            qs.append(options.album)

        query = {
                'query': " ".join(qs)
                }

        result = self.api.call_search2(query=query)
        songs = SongList(self._getList(result['searchResult2'], 'song'))

        return songs

    def search_artist(self, options):
        query = {
                'query': options.artist
                }
        result = self.api.call_search2(query=query)

        artists = ArtistList(self._getList(result['searchResult2'], 'artist'))
        return artists

unicode_re = re.compile(r'&#[0-9]{1,7};')

class SearchList(object):

    def __init__(self, entries):
        self.entries = makeArray(entries)
        self.length = len(self.entries)

    def entryString(self, entry):
        return unicode(entry)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        fmt = u"%%%dd. %%s" % (len(str(self.length)))

        cnt = 0
        strings = []

        def replacer(s):
            word = s.group()
            return unichr(int(word[2:-1]))

        for entry in self.entries:
            cnt += 1
            encoded_str = unicode_re.sub(
                    replacer,
                    unicode(self.entryString(entry))
                    )
            strings.append(fmt % (cnt, encoded_str))

        return u"\n".join(strings).encode('utf-8')

    def __repr__(self):
        return pretty(self.entries)

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, key):
        return self.entries[key]


class ArtistList(SearchList):
    def entryString(self, entry):
        return unicode(entry['name'])


class SongList(SearchList):
    def entryString(self, entry):
        return u"%s - %s - %s - %s" % (entry['album'], entry['track'],
                entry['artist'], entry['title'])

