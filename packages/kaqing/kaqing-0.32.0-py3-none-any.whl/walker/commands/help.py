from walker.commands.command import Command, repl_cmds
from walker.repl_state import ReplState
from walker.utils import lines_to_tabular, log

class Help(Command):
    COMMAND = 'help'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Help, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Help.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        lines = [c.help(state) for c in repl_cmds if c.help(state)]
        log(lines_to_tabular(lines, separator=':'))

        return lines

    def completion(self, _: ReplState):
        return {Help.COMMAND: None}

    def help(self, _: ReplState):
        return None