"""Module level config."""
import os
from enum import Enum
from pathlib import Path


NOTES_DIR = Path(os.path.join(
    os.environ['HOME'], 'bronotes'
))


# TODO Finish this
class Cfg():
    """Represent the bronotes config.

    Merges multiple levels of config and manages a single source of truth.
    Reads from defaults, flags, and user defined files.
    """

    def __init__(self):
        """Construct the config manager."""
        self.dir = NOTES_DIR

    def init(self):
        """Post-construction initialization.

        Will probably be needed in the future to handle some cli arguments.
        """
        self.__test_dir()

    def __test_dir(self):
        """Create the notes dir if it doesn't exist."""
        if not os.path.exists(self.dir):
            try:
                os.mkdir(self.dir)
            except OSError:
                print(f"Creation of the directory {self.cfg.dir} failed.")
            else:
                print(
                    f"Successfully created the directory {self.cfg.dir}.")


class Text(Enum):
    """Module-level text constants.

    Text objects currently know 3 prefixes:
        * I_ = info
        * W_ = warning
        * E_ = error
    """

    I_FILE_EXISTS = 'File already exists.'
    I_DIR_EXISTS = 'Directory already exists.'
    I_NO_DIR = 'No such directory to list.'
    I_EDIT_FINISHED = 'Finished editting the file.'
    E_FILE_NOT_FOUND = 'Error creating file, did you mean to use -r?'
    E_NO_SUCH = 'No such file or directory.'
    E_EDITTING = 'Encountered an error editting.'
    E_DIR_NOT_EMPTY = 'Dir not empty, try -r.'
    E_NOT_A_DIR = "That's note a directory, unable to create file."
