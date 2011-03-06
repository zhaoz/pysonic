"""clisonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

import base64
import simplejson
import urllib
import urllib2
import urlparse

class Clisonic(object):

    def __init__(self, uri, version="1.5.0", client="clisonic", json=True,
                 username=None, password=None):
        self.uri_parts = urlparse.urlparse(uri)

        self.params = {
                    'v': version,
                    'c': client,
                    'f': ('xml', 'json')[json]
                }

        if self.uri_parts.scheme == 'https':
            self.conn = httplib.HTTPSConnection
        else:
            self.conn = httplib.HTTPConnection

        self.username = (self.uri_parts.username, username)[username != None]
        self.password = (self.uri_parts.password, password)[password != None]
        self.uri_parts.username = ""
        self.uri_parts.password = ""

        self.base_url = urlparse.urlunparse(self.uri_parts)

        self.passman = urllib2.HTTPPasswordMgrWithDeafultRealm()

        self.passman.add_password(None, self.buildUrl(),
                self.username, self.password)

        self.auth_handler = urllib2.HTTPBaseicAuthHandler(self.passman)

        self.opener = urllib2.build_opener(self.auth_handler)

        urllib2.install_opener(opener)


    def buildUrl(self, method="", query={}):

        for name, val in self.params.items():
            if name not in query:
                query[name] = val

        return "%s/rest/%s%s" % (self.base_url, method, urllib.urlencode(query))

    def _request(self, url, data=None, headers=None):
        req = urllib2.Request(url)

        for key in headers:
            req.add_header(key, headers[key])

        return req


    def ping(self):
        url = self.buildUrl('ping')
        req = self._request(url)
        resp = urllib2.urlopen(req)

        print response.read()
