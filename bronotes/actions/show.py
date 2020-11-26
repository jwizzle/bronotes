"""Action to show the contents of a note."""
import os
import logging
import pyperclip
from pathlib import Path
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text


class ActionShow(BronoteAction):
    """Show the contents of a note."""

    action = 'show'
    arguments = {
        'note': {
            'help': 'The note to show.',
            'nargs': None
        }
    }
    flags = {
        '--copy': {
            'short': '-c',
            'action': 'store_true',
            'help': 'Copy file contents to clipboard.'
        },
        '--search': {
            'short': '-s',
            'action': 'store_true',
            'help': 'Search for a file instead of using a hard path.'
        }
    }

    def init(self, args):
        """Construct the action."""
        if not args.search:
            self.note = Path(os.path.join(
                self.cfg.dir, args.note))
        else:
            self.note = self.find_note(args.note)
        self.copy = args.copy

    def process(self):
        """Process this action."""
        try:
            if os.path.isfile(self.note):
                with open(self.note) as note:
                    contents = note.read()

                    if self.copy:
                        pyperclip.copy(contents)

                    return contents
            else:
                return Text.E_NO_SUCH.value
        except Exception as exc:
            logging.debug(exc)
            return 'Error opening note.'
