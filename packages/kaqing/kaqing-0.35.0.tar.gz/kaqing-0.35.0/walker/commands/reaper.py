import click

from walker.commands.command import Command
from walker.commands.command_helpers import ClusterCommandHelper
from walker.commands.reaper_forward import ReaperForward
from walker.commands.reaper_restart import ReaperRestart
from walker.commands.reaper_run_abort import ReaperRunAbort
from walker.commands.reaper_runs import ReaperRuns
from walker.commands.reaper_runs_abort import ReaperRunsAbort
from walker.commands.reaper_schedule_activate import ReaperScheduleActivate
from walker.commands.reaper_schedule_start import ReaperScheduleStart
from walker.commands.reaper_schedule_stop import ReaperScheduleStop
from walker.commands.reaper_schedules import ReaperSchedules
from walker.commands.reaper_status import ReaperStatus
from walker.repl_state import ReplState, RequiredState
from walker.utils import lines_to_tabular, log, log2

class Reaper(Command):
    COMMAND = 'reaper'
    reaper_login = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Reaper, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Reaper.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if state.in_repl:
            log(lines_to_tabular([c.help(ReplState()) for c in Reaper.cmd_list()], separator=':'))

            return 'command-missing'
        else:
            # head with the Chain of Responsibility pattern
            cmds = Command.chain(Reaper.cmd_list())
            if not cmds.run(cmd, state):
                log2('* Command is missing.')
                Command.display_help()

    def cmd_list():
        return [ReaperSchedules(), ReaperScheduleStop(), ReaperScheduleActivate(), ReaperScheduleStart(),
                ReaperForward(), ReaperRunAbort(), ReaperRunsAbort(), ReaperRestart(), ReaperRuns(), ReaperStatus()]

    def completion(self, state: ReplState):
        if state.statefulset:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return None

class ReaperCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Commands:')

        log(lines_to_tabular([c.help(ReplState()).replace(f'{Reaper.COMMAND} ', '  ', 1) for c in Reaper.cmd_list()], separator=':'))
        log()
        ClusterCommandHelper.cluster_help()