"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

import mad
import pyaudio

import pysonic.player.base as base


class MadBackend(base.Backend):

    def play(self):
        mf = mad.MadFile(self.mp3_stream)

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
