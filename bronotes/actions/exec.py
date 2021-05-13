"""Execute a shell command in the notes folder."""
import os
import sys
from bronotes.actions.base_action import BronoteAction


class ActionExec(BronoteAction):
    """Execute a shell command in the notes folder."""

    action = 'exec'
    arguments = {
        'command': {
            'help': 'Command to execute.',
            'nargs': '+',
        }
    }
    flags = {}

    def init(self, args):
        """Construct the action."""
        self.set_attributes(args)

    def process(self):
        """Process the action."""
        command = ' '.join(sys.argv[2:])
        os.chdir(self.cfg.notes_dir)
        result = os.system(command)

        return result
