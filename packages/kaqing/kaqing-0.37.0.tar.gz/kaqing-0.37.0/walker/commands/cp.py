import click
import pyperclip

from walker.commands.command import Command
from walker.commands.command_helpers import ClusterOrPodCommandHelper
from walker.commands.reaper_session import ReaperSession
from walker.k8s_utils import list_pods
from walker.repl_state import ReplState, RequiredState
from walker.utils import lines_to_tabular, log, log2

class ClipboardCopy(Command):
    COMMAND = 'cp'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ClipboardCopy, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ClipboardCopy.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if len(args) < 1:
            if state.in_repl:
                log2('cp <key>')
                log2('Keys:')
                log2(lines_to_tabular([f'{k},{v}' for k, v in self.values(state, collapse=True).items()], separator=','))
            else:
                log2('* Key is missing.')
                Command.display_help()

            return 'command-missing'

        key = args[0]
        value = self.values(state)[key]
        pyperclip.copy(value)
        log2('The following line has been copied to clipboard. Use <Ctrl-V> to use it.')
        log2(f'  {value}')

        return 'value-copied'

    def values(self, state: ReplState, collapse = False):
        d = {}

        pod_names: list[str] = [pod.metadata.name for pod in list_pods(state.statefulset, state.namespace)]

        if collapse:
            pod_names = pod_names[:1]
            pod_names[0] = pod_names[0].replace('-0', '-?')

        d |= {
            f'node-exec-{"?" if collapse else i}': f'kubectl exec -it {pod} -c cassandra -n {state.namespace} -- bash' for i, pod in enumerate(pod_names)
        }

        user, pw = state.user_pass()
        d |= {
            f'nodetool-{"?" if collapse else i}': f'kubectl exec -it {pod} -c cassandra -n {state.namespace} -- nodetool -u {user} -pw {pw}' for i, pod in enumerate(pod_names)
        }

        user, pw = state.user_pass(secret_path='cql.secret')
        d |= {
            f'cql-{"?" if collapse else i}': f'kubectl exec -it {pod} -c cassandra -n {state.namespace} -- cqlsh -u {user} -p {pw}' for i, pod in enumerate(pod_names)
        }

        if reaper := ReaperSession.reaper_spec(state, update_state=False):
            d |= {
                'reaper-exec': reaper["exec"],
                'reaper-forward': reaper["forward"],
                'reaper-ui': reaper["web-uri"],
                'reaper-username': reaper["username"],
                'reaper-password': reaper["password"]
            }

        return d

    def completion(self, state: ReplState):
        return {ClipboardCopy.COMMAND: {key: None for key in self.values(state).keys()}}

    def help(self, _: ReplState):
        return f"{ClipboardCopy.COMMAND} <key>: copy a value to clipboard for conveninence"

class CopyCommandHelper(click.Command):
    def lines(self):
        return [
            'node-exec-?: kubectl exec command to the Cassandra pod',
            'reaper-exec: kubectl exec command to the Reaper pod',
            'reaper-forward: kubectl port-forward command to the Reaper pod',
            'reaper-ui: uri to Reaper ui',
            'reaper-username: Reaper user name',
            'reaper-password: Reaper password',
        ]

    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Keys:')

        log(lines_to_tabular(self.lines(), separator=':'))
        log()
        ClusterOrPodCommandHelper.cluter_or_pod_help()