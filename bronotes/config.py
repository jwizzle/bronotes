"""Module level config."""
import os
import yaml
from pkg_resources import Requirement, resource_filename
from enum import Enum
from pathlib import Path


class Cfg():
    """Represent the bronotes config.

    Merges multiple levels of config and manages a single source of truth.
    Reads from defaults, flags, and user defined files.
    """

    def __init__(self):
        """Construct the config manager."""
        self.cfg_file = resource_filename(
            Requirement.parse('bronotes'), 'bronotes/config.yml')
        with open(self.cfg_file, 'r') as file:
            self.dict = yaml.load(file, Loader=yaml.SafeLoader)

    def init(self):
        """Post-construction initialization."""
        self.__test_notedir()
        self.__load_cfg()

    def set_dir(self, new_dir):
        """Set a new notes directory."""
        self.dict['notes_dir'] = str(new_dir)
        self.__write_cfg()
        self.__load_cfg()

    def enable_autosync(self):
        """Enable auto syncing."""
        self.dict['autosync'] = True
        self.__write_cfg()
        self.__load_cfg()

    def disable_autosync(self):
        """Disable auto syncing."""
        self.dict['autosync'] = False
        self.__write_cfg()
        self.__load_cfg()

    def __write_cfg(self):
        """Write config updates to file."""
        with open(self.cfg_file, 'w') as file:
            yaml.dump(self.dict, file)

    def __load_cfg(self):
        self.dir = Path(self.dict['notes_dir'])
        try:
            self.autosync = self.dict['autosync']
        except KeyError:
            self.autosync = False

    def __test_notedir(self):
        """Create the notes dir if it doesn't exist."""
        if self.dict['notes_dir']:
            if os.path.exists(self.dict['notes_dir']):
                return True

        print(Text.I_NO_CONFIG.value)
        notes_dir = input(
            'Where do you want to keep your notes? (full path): ')

        if not os.path.exists(notes_dir):
            try:
                os.mkdir(notes_dir)
            except OSError:
                print(
                    f"Creation of the directory {notes_dir}\
                    failed.")
            else:
                print(
                    f"Successfully created the directory\
                    {self.dir}.")

        self.dict['notes_dir'] = notes_dir
        self.__write_cfg()


# TODO This was a horrible idea.
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
    I_NO_CONFIG = 'No configuration detected.'
    I_CONFIG_UPDATE = 'Updated config.'
    E_FILE_NOT_FOUND = 'Error creating file, did you mean to use -r?'
    E_NO_SUCH = 'No such file or directory.'
    E_EDITTING = 'Encountered an error editting.'
    E_DIR_NOT_EMPTY = 'Dir not empty, try -r.'
    E_NOT_A_DIR = "That's note a directory, unable to create file."


cfg = Cfg()
