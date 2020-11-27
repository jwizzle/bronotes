"""Action to sync the notes dir with git."""
import os
from git import Repo
from git.exc import InvalidGitRepositoryError
from pathlib import Path
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text


class ActionSync(BronoteAction):
    """Sync the notes dir with git."""

    action = 'sync'
    arguments = {}
    flags = {}

    def init(self, args):
        """Construct the action."""
        pass

    def process(self):
        """Process this action."""
        repo = self.sync()

        return repo
