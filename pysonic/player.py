"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

import ao
import mad

from pysonic.api import Subsonic


class SubPlayer(object):

    def __init__(self, subsonic=None, backend="pulse"):
        self.sub = subsonic
        self.backend = backend

    def play(self, song=None, song_id=None):
        if not song_id:
            song_id = song["id"]

        sub_stream = self.sub.call_stream(query={"id": song_id})

        inst = MadDecoder(sub_stream, backend=self.backend)
        inst.play()


class Decoder(object):
    def __init__(self, mp3_stream, backend="pulse"):
        self.mp3_stream = mp3_stream
        self.backend = backend

    def _playStream(self, stream, sample_rate=None):

        dev = ao.AudioDevice(self.backend, rate=sample_rate)

        buf = stream.read()
        while buf:
            dev.play(buf, len(buf))
            buf = stream.read()


class MadDecoder(Decoder):

    def play(self):
        mf = mad.MadFile(self.mp3_stream)
        self._playStream(mf, sample_rate=mf.samplerate())
