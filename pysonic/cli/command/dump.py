"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.com>'

import pysonic
from pysonic.cli.command import command
import pysonic.cli.command.base as base

@command
class DumpCommand(base.BaseCommand):
    COMMANDS = ['dump']

    def __call__(self, cli, args):
        """Dump json representation."""

        cmd = args.pop(0)

        if not cli.cur_list:
            print "No list to operate on."
            return

        if len(args) < 1:
            print repr(cli.cur_list)
            return

        try:
            num = int(args[0]) - 1
            print pysonic.pretty(cli.cur_list[num])
        except ValueError, ex:
            print "Wrong format"
