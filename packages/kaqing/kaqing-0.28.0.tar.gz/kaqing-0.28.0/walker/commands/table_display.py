from walker.checks.check_utils import run_checks
from walker.columns.columns import Columns, collect_checks
from walker.commands.issues import Issues
from walker.repl_state import ReplState
from walker.utils import lines_to_tabular, log

def show_table(state: ReplState, pods: list[str], cols: str, header: str, show_output=False):
    columns = Columns.create_columns(cols)

    results = run_checks(cluster=state.statefulset, pod=state.pod, namespace=state.namespace, checks=collect_checks(columns), show_output=show_output)

    def line(pod_name: str):
        cells = [c.pod_value(results, pod_name) for c in columns]
        return ','.join(cells)

    lines = [line(pod) for pod in pods]
    lines.sort()

    log(lines_to_tabular(lines, header, separator=','))

    Issues.show(results)