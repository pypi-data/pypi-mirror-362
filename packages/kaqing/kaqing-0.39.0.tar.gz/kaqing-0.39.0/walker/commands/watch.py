import threading
import time
from kubernetes import client
from typing import List

from walker.commands.command import Command
from walker.commands.display_utils import show_pods
from walker.config import Config
from walker.repl_state import ReplState, RequiredState
from walker.k8s_utils import list_pods, list_statefulset_names
from walker.utils import log2

class Watch(Command):
    COMMAND = 'watch'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Watch, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Watch.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        pods = list_pods(state.statefulset, state.namespace)
        if not pods:
            log2("No pods are found.")
            return state

        stop_event = threading.Event()
        thread = threading.Thread(target=self.loop, args=(stop_event, pods, state.namespace))
        thread.start()

        try:
            log2(f"Press Ctrl+C to break.")

            time.sleep(Config().get('watch.timeout', 3600 * 1))
        except KeyboardInterrupt:
            pass

        log2("Stopping watch...")
        stop_event.set()
        thread.join()

        return state

    def loop(self, stop_flag, pods: List[client.V1Pod], ns: str):
        show_pods(pods, ns)

        cnt = Config().get('watch.interval', 10)
        while not stop_flag.is_set():
            time.sleep(1)
            cnt -= 1

            if not cnt:
                show_pods(pods, ns)
                cnt = Config().get('watch.interval', 10)

    def completion(self, state: ReplState):
        if state.pod:
            return {}

        if not state.statefulset:
            return {Watch.COMMAND: {n: None for n in list_statefulset_names()}}

        return {Watch.COMMAND: None}

    def help(self, _: ReplState):
        return f'{Watch.COMMAND}: watch pod changes'