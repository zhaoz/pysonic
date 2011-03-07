"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

from pysonic.api import Subsonic


class SubPlayer(object):

    def __init__(self, subsonic=None, playend="mad"):
        self.sub = subsonic

        if playend == 'mad':
            from pysonic.player.madbackend import MadBackend
            self.backend = MadBackend
        else:
            from pysonic.player.madbackend import MadBackend
            self.backend = MadBackend

    def play(self, song=None, song_id=None):
        if not song_id:
            song_id = song["id"]

        sub_stream = self.sub.call_stream(query={"id": song_id})

        inst = self.backend(sub_stream)
        inst.play()
