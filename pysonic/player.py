"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

from pysonic.api import Subsonic

import mad
import pyaudio


class SubPlayer(object):

    def __init__(self, subsonic=None):
        self.sub = subsonic

        ret = self.sub.call_search(query={"artist": "Yelle"})

        self.play(ret["match"])

    def play(self, song):

        sub_stream = self.sub.call_stream(query={"id": song["id"]})

        mf = mad.MadFile(sub_stream)

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(pyaudio.paInt32),
                channels = 2,
                rate = mf.samplerate(),
                output = True)

        data = mf.read()

        while data != None:
            stream.write(data)
            data = mf.read()

        stream.close()
        p.terminate()
