"""Edit a note or directory."""
import os
import logging
from pathlib import Path
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text


class ActionEdit(BronoteAction):
    """Edit a note."""

    action = 'edit'
    arguments = {
        'file': {
            'help': 'The file to edit',
            'nargs': None
        }
    }
    flags = {
        '--search': {
            'short': '-s',
            'action': 'store_true',
            'help': 'Search for a file instead of using a hard path.'
        }
    }

    def init(self, args):
        """Construct the action."""
        if not args.search:
            self.path = Path(os.path.join(
                self.cfg.dir, args.file))
        else:
            self.path = self.find_note(args.file)

    def process(self):
        """Process the action."""
        if self.path is None:
            return Text.E_NO_SUCH.value

        try:
            os.system(f"{os.getenv('EDITOR')} {self.path}")
            return Text.I_EDIT_FINISHED.value
        except Exception as exc:
            logging.error(exc)
            return Text.E_EDITTING.value
