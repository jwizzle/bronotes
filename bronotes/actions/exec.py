"""Execute a shell command in the notes folder.

Todo:
    * Figure out a way to get zsh completion for subcommands
"""
import os
from bronotes.actions.base_action import BronoteAction


class ActionExec(BronoteAction):
    """Execute a shell command in the notes folder.

    Swallows all following args.
    """

    action = 'exec'
    arguments = {}
    flags = {}

    def init(self, args):
        """Construct the action."""
        pass

    def process(self, extra_args):
        """Process the action."""
        command = ' '.join(extra_args)
        os.chdir(self.cfg.notes_dir)
        result = os.system(command)

        return f"Command exited with {result}."
