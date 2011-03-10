"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

from ConfigParser import RawConfigParser
import os

import simplejson

def pretty(json):
    return simplejson.dumps(json, sort_keys=True, indent=4 * ' ')

config_defaults = {
    'general': {
        'debug': False
        },
    "playback": {
        "backend": "auto"
        }
    }

def ReadConfig(f=None):
    user_config = RawConfigParser({
        'debug': False,
        'backend': 'auto'
        })

    if not f:
        f = "%s/.pysonicrc" % (os.path.expanduser('~'))

    user_config.read(f)

    return user_config
