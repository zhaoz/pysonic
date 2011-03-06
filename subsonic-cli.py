#!/usr/bin/python2

import simplejson

import clisonic

USER="test"
PW='test'
URL="https://localhost/subsonic"

def prettyPrint(json):
    print simplejson.dumps(json, sort_keys=True, indent=4 * ' ')


def main():
    sub = clisonic.SubsoniceAPI(URL, username=USER, password=PW)

    ret = sub.call_search(query={"artist": "Yelle"})

    song_id = ret["match"][0]["id"]

    resp = sub.call_stream(query={"id": song_id})

if __name__ == "__main__":
    main()
