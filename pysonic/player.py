"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

import ao
import mad

from pysonic.api import Subsonic


class SubPlayer(object):

    def __init__(self, subsonic=None, playend="mad"):
        self.sub = subsonic

        if playend == 'mad':
            self.backend = MadBackend
        else:
            self.backend = MadBackend

    def play(self, song=None, song_id=None):
        if not song_id:
            song_id = song["id"]

        sub_stream = self.sub.call_stream(query={"id": song_id})

        inst = self.backend(sub_stream)
        inst.play()


class Backend(object):
    def __init__(self, mp3_stream, backend="pulse"):
        self.mp3_stream = mp3_stream
        self.backend = backend

    def _playStream(self, stream, sample_rate=None):

        dev = ao.AudioDevice(self.backend, rate=sample_rate)

        buf = stream.read()
        while buf:
            dev.play(buf, len(buf))
            buf = stream.read()


class MadBackend(Backend):

    def play(self):
        mf = mad.MadFile(self.mp3_stream)
        self._playStream(mf, sample_rate=mf.samplerate())
