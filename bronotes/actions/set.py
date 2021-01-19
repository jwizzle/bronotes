"""Set the bronotes config."""
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text
from pathlib import Path


class ActionSet(BronoteAction):
    """Set config options."""

    action = 'set'
    arguments = {}
    flags = {
        '--dir': {
            'short': '-d',
            'action': 'store',
            'help': 'The new notes directory to use.'
        },
        '--sync': {
            'short': '-s',
            'action': 'store',
            'help': 'Autosync (yes/no/true/false)'
        },
        '--default': {
            'short': '-D',
            'action': 'store',
            'help': 'The default action to take if an argument is not known.'
        },
    }

    def init(self, args):
        """Construct the action."""
        if args.dir:
            self.dir = Path(args.dir)
        else:
            self.dir = False

        if args.sync:
            self.sync = args.sync
        else:
            self.sync = None

        if args.default:
            self.default = args.default
        else:
            self.default = False

    def process(self):
        """Process the action."""
        if self.dir:
            self.cfg.set_dir(self.dir)

        if self.sync is not None:
            if self.sync in ['yes', 'true']:
                self.cfg.enable_autosync()
            elif self.sync in ['no', 'false']:
                self.cfg.disable_autosync()

        if self.default:
            self.cfg.set_default_action(self.default)

        return Text.I_CONFIG_UPDATE.value
