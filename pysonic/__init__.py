"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

import simplejson

def pretty(json):
    return simplejson.dumps(json, sort_keys=True, indent=4 * ' ')
