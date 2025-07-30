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

    @DyngleCommand.wrap
    def execute(self):
        flows = self.app.config.get('dyngle-flows')

        if not flows:
            raise RuntimeError('No flows configured')

        if self.flow not in flows:
            raise RuntimeError(f'Flow "{self.flow}" not found')

        tasks = flows[self.flow]

        for task_str in tasks:
            # Split task string at spaces and pass to subprocess
            task_parts = task_str.split()
            result = subprocess.run(task_parts)

            if result.returncode != 0:
                raise RuntimeError(f'Task failed: {task_str}')

        return f'Flow "{self.flow}" completed successfully'
