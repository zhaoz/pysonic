"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

import base64
import simplejson
from socket import gethostname
import urllib
import urllib2
import urlparse


class Subsonic(object):

    def __init__(self, config, version="1.5.0", json=True, client=None):

        self.config = config
        self.uri_parts = urlparse.urlparse(config.get('general', 'server'))

        if not client:
            client = gethostname()

        self.username = config.get('general', 'username')
        self.password = config.get('general', 'password')

        self.base_url = urlparse.urlunsplit(
                urlparse.SplitResult(self.uri_parts.scheme, self.uri_parts.netloc,
                    self.uri_parts.path, "", ""))

        self.params = {
                    'v': version,
                    'c': client,
                    'f': ('xml', 'json')[json],
                    'u': self.username,
                    'p': self.password
                }

        self.debug = config.get('general', 'debug')

        # WHY YOU STILL WORK!?
        #self._init_opener()

    def _init_opener(self):
        self.passman = urllib2.HTTPPasswordMgrWithDefaultRealm()

        self.passman.add_password(None, self.buildUrl(),
                self.username, self.password)
        self.auth_handler = urllib2.HTTPBasicAuthHandler(self.passman)

        self.opener = urllib2.build_opener(self.auth_handler)

        urllib2.install_opener(self.opener)


    def buildUrl(self, method="", query={}):

        for name, val in self.params.items():
            if name not in query:
                query[name] = val

        path = '%s/rest/%s.view' % (self.uri_parts.path, method)

        url = urlparse.urlunsplit((self.uri_parts.scheme, self.uri_parts.netloc,
                path, urllib.urlencode(query), ""))

        return url

    def _request(self, url, data=None, headers={}):
        req = urllib2.Request(url)

        for key in headers:
            req.add_header(key, headers[key])

        return req

    def callMethod(self, method, query={}, headers={}):
        url = self.buildUrl(method, query=query)

        if self.debug:
            print "Calling method: %s" % (url)

        req = self._request(url, headers=headers)
        response = urllib2.urlopen(req)

        return response

    def handle_search(self, resp):
        js = self.json_handler(resp)

        return js["subsonic-response"]["searchResult"]

    def handle_stream(self, resp):
        return resp

    def json_handler(self, resp):
        js = simplejson.load(resp)

        return js["subsonic-response"]

    def print_handler(self, resp):
        print resp.read()

    def __getattr__(self, method):
        if not method[:5] == "call_":
            raise AttributeError("No method")

        method = method[5:]

        def wrapped_call(*args, **kwargs):
            resp = self.callMethod(method, *args, **kwargs)

            after = 'handle_%s' % (method)
            ret = None

            if hasattr(self, after):
                ret = getattr(self, after)(resp)
            else:
                ret = self.json_handler(resp)

            return ret

        return wrapped_call

