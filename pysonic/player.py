"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

import threading

import ao
import mad

from pysonic.api import Subsonic


class SubPlayer(object):

    def __init__(self, subsonic=None):
        self.sub = subsonic
        self.backend = subsonic.config.get('playback', 'backend')
        self.cur_play = None

    def getStream(self, song_id):
        return self.sub.call_stream(query={"id": song_id})

    def play(self, song=None, song_id=None):
        if not song_id:
            song_id = song["id"]

        if self.cur_play:
            curT = self.cur_play
            curT.join()

        self.cur_play = PlayerThread(self, song_id, backend=self.backend)
        self.cur_play.start()

    def stop(self):
        if not self.cur_play:
            return

        self.cur_play.stop()
        self.cur_play.join()


class PlayerThread(threading.Thread):

    def __init__(self, player, song_id, backend="auto"):
        self.player = player
        self.song_id = song_id
        self.backend = backend

        self._stop = threading.Event()

        super(PlayerThread, self).__init__()

    def run(self):
        stream = self.player.getStream(self.song_id)

        mf = mad.MadFile(stream)
        dev = ao.AudioDevice(self.backend, rate=mf.samplerate())

        buf = mf.read()
        while buf and not self.stopped():
            dev.play(buf, len(buf))
            buf = mf.read()

        self.player.cur_play = None

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
