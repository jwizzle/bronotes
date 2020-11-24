import pytest
from bronotes.config import NOTES_DIR


class TestConfig():

    def test_constructor(self, cfg_fixt, dir_fixt):
        assert cfg_fixt.dir == dir_fixt
