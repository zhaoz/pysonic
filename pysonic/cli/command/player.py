"""pysonic library.
"""

__author__ = 'Ziling Zhao <zilingzhao@gmail.com>'

from pysonic.cli.command import command
import pysonic.cli.command.base as base


@command
class PlayerCommand(base.BaseCommand):
    COMMANDS = ['play', 'stop']

    def __call__(self, cli, args):
        cmd = args.pop(0)

        if cmd == 'play':
            self.play(cli, args)
        elif cmd == 'stop':
            self.stop(cli, args)

    def play(self, cli, args):
        """Play something."""

        try:
            num = int(args[0]) - 1
            cli.player.play(cli.cur_list[num])
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
            cli.player.play(song_id=args[0])

    def stop(self, cli, args):
        cli.player.stop()
