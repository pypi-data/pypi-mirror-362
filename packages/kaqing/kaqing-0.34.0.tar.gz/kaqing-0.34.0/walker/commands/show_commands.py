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

        user, pw = state.user_pass()

        if state.pod:
            k = f'kubectl exec -it {state.pod} -c cassandra -n {state.namespace}'
        else:
            k = f'kubectl exec -it {state.statefulset}-? -c cassandra -n {state.namespace}'

        cmds = [
            f'bash,{k} -- bash',
            f'nodetool,{k} -- nodetool -u {user} -pw {pw}'
        ]

        if reaper := ReaperSession.reaper_pod_from_cluster(state, update_state=False):
            user, pw = state.user_pass(secret_path='reaper.secret')
            local_port = Config().get('reaper.port-forward.local-port', 9001)
            cmds.append(f'reaper,kubectl exec -it {reaper} -n {state.namespace} -- bash')
            cmds.append(f',kubectl port-forward pods/{reaper} -n {state.namespace} {local_port}:8080')
            cmds.append(f',http://localhost:{local_port}/web-ui')
            cmds.append(f',{user}:{pw}')

        log(lines_to_tabular(cmds, separator=','))

        return cmds

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f"{ShowKubectlCommands.COMMAND}: show kubectl commands"