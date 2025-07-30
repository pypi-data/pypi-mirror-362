from walker.commands.command import Command
from walker.repl_state import ReplState, RequiredState
from walker.k8s_utils import cassandra_nodes_exec, cassandra_pod_exec, get_user_pass

class ShowVersion(Command):
    COMMAND = 'show version'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowVersion, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowVersion.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, _ = state.apply_args(args)
        if not self.validate_state(state):
            return state

        user, pw = get_user_pass(state.statefulset if state.statefulset else state.pod, state.namespace, secret_path='cql.secret')
        command = f'cqlsh -u {user} -p {pw} -e "show version"'

        if state.pod:
            return cassandra_pod_exec(state.pod, state.namespace, command)
        else:
            return cassandra_nodes_exec(state.statefulset, state.namespace, command, action='cql')

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{ShowVersion.COMMAND}: show Cassandra version'