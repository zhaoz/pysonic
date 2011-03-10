"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.coM>'

from optparse import OptionParser
import re
import readline
import shlex
import sys

import pysonic
from pysonic.api import Subsonic
from pysonic.player import SubPlayer

import commands

instance = None

class PySubCli(object):

    def __init__(self, config):

        self.api = Subsonic(config)
        self.player = SubPlayer(subsonic=self.api)

        self._cur_list = None

        global instance
        instance = self

        commands.register_all()

    @property
    def cur_list(self):
        return self._cur_list

    @cur_list.setter
    def cur_list(self, lst):
        self._cur_list = lst

    def dump(self, args):
        """Dump json representation."""
        if not self.cur_list:
            print "No list to operate on."
            return

        if len(args) < 1:
            print repr(self.cur_list)
            return

        try:
            num = int(args[0])
            print pysonic.pretty(self.cur_list[num])
        except ValueError, ex:
            print "Wrong format"


    def play(self, args):
        """Play something."""

        try:
            num = int(args[0]) - 1
            self.player.play(self.cur_list[num])
            return
        except IndexError, ex:
            print "That's not in the list."
            return
        except ValueError, ex:
            # don't care about this
            pass

        # maybe its an ID?
        id_re = re.compile(r'^[a-f0-9]+$')

        if id_re.match(args[0]):
            self.player.play(song_id=args[0])

    def stop(self, args):
        self.player.stop()

    def execArgs(self, args):
        """Execute commands given on the cli."""
        cmd = commands.find(args)

        cmd(self.api, args)


        #if cmd == 'search':
            #self.searchArgs(args[1:])
        #elif cmd == 'relist':
            #print self.cur_list
        #elif cmd == 'dump':
            #self.dump(args[1:])
        #elif cmd == 'play':
            #self.play(args[1:])
        #elif cmd == 'stop':
            #self.stop(args[1:])

    def exit(self, state):
        # kill any player threads
        self.player.stop()
        sys.exit(state)

    def shell(self):
        while True:
            try:
                raw = raw_input(">>> ")
            except EOFError, ex:
                print "\nExiting"
                self.exit(0)
            except KeyboardInterrupt, ex:
                print "\nInteruptted -- Exiting"
                self.exit(0)

            self.execArgs(shlex.split(raw))
