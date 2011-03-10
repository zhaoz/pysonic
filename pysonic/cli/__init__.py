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

import command

class PySubCli(object):

    def __init__(self, config):

        self.api = Subsonic(config)
        self.player = SubPlayer(subsonic=self.api)

        self._cur_list = None

        command.register_all()

    @property
    def cur_list(self):
        return self._cur_list

    @cur_list.setter
    def cur_list(self, lst):
        self._cur_list = lst


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
        cmd = command.find(args)

        cmd(self, args)

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
