import datetime
from kubernetes import client
from kubernetes.client.rest import ApiException

from walker.commands.command import Command
from walker.repl_state import ReplState, RequiredState
from walker.utils import log2

class RollingRestart(Command):
    COMMAND = 'rollout'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RollingRestart, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RollingRestart.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        self.rolling_restart(state.statefulset, state.namespace)

        return state

    def rolling_restart(self, statefulset, namespace):
        # kubectl rollout restart statefulset <statefulset-name>
        v1_apps = client.AppsV1Api()

        now = datetime.datetime.now(datetime.timezone.utc)
        now = str(now.isoformat("T") + "Z")
        body = {
            'spec': {
                'template':{
                    'metadata': {
                        'annotations': {
                            'kubectl.kubernetes.io/restartedAt': now
                        }
                    }
                }
            }
        }

        try:
            v1_apps.patch_namespaced_stateful_set(statefulset, namespace, body, pretty='true')
        except ApiException as e:
            log2("Exception when calling AppsV1Api->read_namespaced_statefulset_status: %s\n" % e)

    def completion(self, state: ReplState):
        if state.pod:
            return {}
        elif state.statefulset:
            return {RollingRestart.COMMAND: None}

        return {}

    def help(self, _: ReplState):
        return f'{RollingRestart.COMMAND}: rolling restart all nodes'