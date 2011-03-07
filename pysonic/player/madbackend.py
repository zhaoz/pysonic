"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

import ao
import mad

import pysonic.player.base as base


class MadBackend(base.Backend):

    def play(self):
        mf = mad.MadFile(self.mp3_stream)

        dev = ao.AudioDevice("pulse", rate=mf.samplerate())

        buf = mf.read()
        while buf:
            dev.play(buf, len(buf))
            buf = mf.read()

