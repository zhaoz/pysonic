#!/usr/bin/python2

import clisonic

USER="test"
PW='test'
URL="https://localhost/subsonic"


def main():

    sub = clisonic.Clisonic(URL, username=USER, password=PW)

    sub.ping()


if __name__ == "__main__":
    main()
