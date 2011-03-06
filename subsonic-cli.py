#!/usr/bin/python2

import clisonic

USER="test"
PW='test'
URL="https://localhost/subsonic"


def main():

    sub = clisonic.Clisonic(URL, username=USER, password=PW)
    sub.call_ping()

    sub.call_getNowPlaying()


if __name__ == "__main__":
    main()
