"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

def makeArray(obj):
    if type(obj) is not list:
        return [obj,]
    return obj

class Search(object):
    def __init__(self, api):
        self.api = api

    def search_song(self, options):
        query = {
                'query': options.song
                }

        result = self.api.call_search2(query=query)
        songs = SongList(result['searchResult2']['song'])

        return songs

    def search_artist(self, options):
        query = {
                'query': options.artist
                }
        result = self.api.call_search2(query=query)
        artists = ArtistList(result['searchResult2']['artist'])
        return artists

class SearchList(object):

    def __init__(self, entries):
        self.entries = makeArray(entries)
        self.length = len(entries)

    def entryString(self, entry):
        return str(entry)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        fmt = "%%%dd. %%s" % (len(str(self.length)))

        cnt = 0
        strings = []

        for entry in self.entries:
            cnt += 1
            strings.append(fmt % (cnt, self.entryString(entry)))

        return "\n".join(strings)

class ArtistList(SearchList):
    def entryString(self, entry):
        return entry['name']

class SongList(SearchList):
    def entryString(self, entry):
        return "%s - %s - %s - %s" % (entry['album'],
            entry['track'], entry['artist'], entry['title'])

