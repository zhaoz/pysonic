#!/usr/bin/python2

import simplejson

import mad
import pyaudio

from pysonic import SubsonicAPI

USER="test"
PW='test'
URL="https://localhost/subsonic"

def prettyPrint(json):
    print simplejson.dumps(json, sort_keys=True, indent=4 * ' ')

class SubsonicPlayer(object):

    def __init__(self):
        self.sub = SubsonicAPI(URL, username=USER, password=PW)

        ret = self.sub.call_search(query={"artist": "Yelle"})

        prettyPrint(ret)
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

def main():
    SubsonicPlayer()

if __name__ == "__main__":
    main()
