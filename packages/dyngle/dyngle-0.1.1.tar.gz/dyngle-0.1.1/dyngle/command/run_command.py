import subprocess
from wizlib.parser import WizParser

from dyngle.command import DyngleCommand


class RunCommand(DyngleCommand):
    """Run a workflow defined in the configuration"""

    name = 'run'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('flow', help='Flow name to run')

    def handle_vals(self):
        super().handle_vals()
        if not self.provided('flow'):
            self.flow = self.app.ui.get_input('Enter flow name: ')

    def _validate_flow_exists(self, flows):
        """Validate that the requested flow exists in configuration"""
        if not flows:
            raise RuntimeError('No flows configured')

        if self.flow not in flows:
            available_flows = ', '.join(flows.keys())
            raise RuntimeError(
                f'Flow "{self.flow}" not found. " + \
                    f"Available flows: {available_flows}')

    def _execute_task(self, task_str):
        """Execute a single task and handle errors"""
        task_parts = task_str.split()
        result = subprocess.run(task_parts)

        if result.returncode != 0:
            raise RuntimeError(
                f'Task failed with code {result.returncode}: {task_str}')

    @DyngleCommand.wrap
    def execute(self):
        flows = self.app.config.get('dyngle-flows')
        self._validate_flow_exists(flows)

        tasks = flows[self.flow]
        for task_str in tasks:
            self._execute_task(task_str)

        return f'Flow "{self.flow}" completed successfully'
