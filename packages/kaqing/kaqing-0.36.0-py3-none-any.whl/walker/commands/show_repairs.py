from walker.commands.command import Command
from walker.repl_state import ReplState, RequiredState
from walker.k8s_utils import cassandra_nodes_exec, cassandra_pod_exec, get_user_pass

class ShowRepairs(Command):
    COMMAND = 'show repairs'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowRepairs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowRepairs.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, _ = state.apply_args(args)
        if not self.validate_state(state):
            return state

        user, pw = state.user_pass()
        command = f"nodetool -u {user} -pw {pw} repair_admin list"

        if state.pod:
            return cassandra_pod_exec(state.pod, state.namespace, command)
        else:
            return cassandra_nodes_exec(state.statefulset, state.namespace, command, action='nodetool')

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{ShowRepairs.COMMAND}: show Cassandra repairs'