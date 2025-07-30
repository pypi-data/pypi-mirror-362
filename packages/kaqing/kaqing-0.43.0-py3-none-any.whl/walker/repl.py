import re
import click
from kubernetes import client
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import PromptSession

from walker.cli_group import cli
from walker.commands.cp import ClipboardCopy
from walker.commands.reaper_forward_stop import ReaperForwardStop
from walker.commands.show_app_id import ShowAppId
from walker.commands.bash import Bash
from walker.commands.cd import Cd
from walker.commands.check import Check
from walker.commands.command import Command
from walker.commands.command_helpers import ClusterCommandHelper
from walker.commands.cqlsh import Cqlsh
from walker.commands.exit import Exit
from walker.commands.param_get import GetParam
from walker.commands.help import Help
from walker.commands.issues import Issues
from walker.commands.ls import Ls
from walker.commands.nodetool import NodeTool
from walker.commands.process import Process
from walker.commands.reaper import Reaper
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
from walker.commands.report import Report
from walker.commands.restart import Restart
from walker.commands.rolling_restart import RollingRestart
from walker.commands.param_set import SetParam
from walker.commands.params_show import ShowParams
from walker.commands.show import Show
from walker.commands.show_commands import ShowKubectlCommands
from walker.commands.show_repairs import ShowRepairs
from walker.commands.show_version import ShowVersion
from walker.commands.status import Status
from walker.commands.storage import Storage
from walker.commands.watch import Watch
from walker.repl_session import ReplSession
from walker.repl_state import ReplState
from walker.k8s_utils import init_config, init_params
from walker.utils import deep_merge_dicts, lines_to_tabular, log2

def enter_repl(state: ReplState):
    cmd_list: list[Command] = [Bash(), Cd(), Check(), ClipboardCopy(), Cqlsh(), GetParam(), Help(), Issues(), Ls(), NodeTool(),
                               Process(),
                               ReaperForwardStop(), ReaperForward(), ReaperSchedules(), ReaperRunAbort(), ReaperRunsAbort(), ReaperRuns(),
                               ReaperScheduleActivate(), ReaperScheduleStop(), ReaperScheduleStart(), ReaperRestart(),
                               ReaperStatus(),
                               Reaper(), Report(), Restart(), RollingRestart(), SetParam(),
                               ShowAppId(), ShowKubectlCommands(), ShowParams(), ShowRepairs(), ShowVersion(), Show(),
                               Status(), Storage(), Watch(),
                               Exit()]
    # head with the Chain of Responsibility pattern
    cmds: Command = Command.chain(cmd_list)
    session = ReplSession().prompt_session

    def prompt_msg():
        msg = ''
        if state.pod:
            # cs-d0767a536f-cs-d0767a536f-default-sts-0
            group = re.match(r".*?-.*?-(.*)", state.pod)
            msg = group[1]
        elif state.statefulset:
            # cs-d0767a536f-cs-d0767a536f-default-sts
            group = re.match(r".*?-.*?-(.*)", state.statefulset)
            msg = group[1]

        return f"{msg}$ " if state.bash_session else f"{msg}> "

    apps_v1_api = client.AppsV1Api()
    statefulsets = apps_v1_api.list_stateful_set_for_all_namespaces(label_selector="app.kubernetes.io/name=cassandra")
    ss = [(statefulset.metadata.name, statefulset.metadata.namespace) for statefulset in statefulsets.items]

    if len(ss) == 0:
        raise Exception("no cassandra statefulsets found")

    while True:
        completer = NestedCompleter.from_nested_dict({})
        if not state.bash_session:
            completions = {}
            for cmd in cmd_list:
                completions = deep_merge_dicts(completions, cmd.completion(state))

            completer = NestedCompleter.from_nested_dict(completions)

        cmd = session.prompt(prompt_msg(), completer=completer)

        if state.bash_session:
            if cmd.strip(' ') == 'exit':
                state.exit_bash()
                continue

            cmd = f'bash {cmd}'

        try:
            if cmd and cmd.strip(' ') and not cmds.run(cmd, state):
                log2(f'* Invalid command: {cmd}')
                log2()
                lines = [c.help(state) for c in cmd_list if c.help(state)]
                log2(lines_to_tabular(lines, separator=':'))
        except Exception as e:
            raise e
            log2(e)

@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ClusterCommandHelper, help="Enter interactive shell.")
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='[cluster]', type=click.UNPROCESSED)
def repl(kubeconfig: str, config: str, param: list[str], cluster:str, namespace: str, extra_args):
    init_config(kubeconfig)
    if not init_params(config, param):
        return

    state = ReplState(ns_statefulset=cluster, namespace=namespace, in_repl=True)
    state, _ = state.apply_args(extra_args)
    enter_repl(state)