from walker.commands.command import Command
from walker.commands.table_display import show_table
from walker.config import Config
from walker.repl_state import ReplState
from walker.k8s_utils import list_pods

class Storage(Command):
    COMMAND = 'storage'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Storage, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Storage.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        args, show_output = Command.extract_options(args, ['-s', '--show'])

        cols = Config().get('storage.columns', 'pod,volume_root,volume_cassandra,snapshots,data,compactions')
        header = Config().get('storage.header', 'POD_NAME,VOLUME /,VOLUME CASS,SNAPSHOTS,DATA,COMPACTIONS')
        if state.pod:
            show_table(state, [state.pod], cols, header, show_output=show_output)
        elif state.statefulset:
            pod_names = [pod.metadata.name for pod in list_pods(state.statefulset, state.namespace)]
            show_table(state, pod_names, cols, header, show_output=show_output)

        return state

    def completion(self, state: ReplState):
        if not state.statefulset:
            return {}

        return {Storage.COMMAND: None}

    def help(self, _: ReplState):
        return f'{Storage.COMMAND}: storage overview'