from walker.commands.command import Command
from walker.commands.reaper_session import ReaperSession
from walker.config import Config
from walker.repl_state import ReplState, RequiredState
from walker.utils import lines_to_tabular, log

class ShowKubectlCommands(Command):
    COMMAND = 'show kubectl-commands'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowKubectlCommands, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowKubectlCommands.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        if not self.validate_state(state):
            return state

        nodetool_user, nodetool_pass = state.user_pass()
        cql_user, cql_pass = state.user_pass(secret_path='cql.secret')

        if state.pod:
            k = f'kubectl exec -it {state.pod} -c cassandra -n {state.namespace}'
        else:
            k = f'kubectl exec -it {state.statefulset}-? -c cassandra -n {state.namespace}'

        cmds = [
            f'bash,{k} -- bash',
            f'nodetool,{k} -- nodetool -u {nodetool_user} -pw {nodetool_pass}',
            f'cql,{k} -- cqlsh -u {cql_user} -p {cql_pass}'
        ]

        if reaper := ReaperSession.reaper_spec(state, update_state=False):
            cmds.append(f'reaper,{reaper["exec"]}')
            cmds.append(f',{reaper["forward"]}')
            cmds.append(f',{reaper["web-uri"]}')
            cmds.append(f',{reaper["username"]}:{reaper["password"]}')

        log(lines_to_tabular(cmds, separator=','))

        return cmds

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f"{ShowKubectlCommands.COMMAND}: show kubectl commands"