"""
Configuration class holds settings loaded from a JSON file (or uses
defaults). Settings contain important paths that are used throughout
the program, and can be modified to contain other data easily.

Copyright (c) 2015 
makos <https://github.com/makos>, chibi <http://neetco.de/chibi>
under GNU GPL v3, see LICENSE for details
"""

import os
import json
import logging

logging.basicConfig(
        filename="log",
        format="[%(lineno)d]%(asctime)s:%(levelname)s:%(message)s",
        level=logging.DEBUG)


class Colors():
    """Terminal escape codes for colored output."""

    RED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    BLACK = '\033[0m'

    # Bold (bright) variants of the same colors above.
    bRED = '\033[1;31m'
    bYELLOW = '\033[1;33m'
    bGREEN = '\033[1;32m'
    bBLUE = '\033[1;34m'
    bBLACK = '\033[1m'


class Config():
    """This class holds config data, paths to important files etc."""

    defaults = {"rootdir": "/srv/sshchan",
                "boardlist_path": "/srv/sshchan/boardlist",
                "postnums_path": "/srv/sshchan/postnums",
                "motd_path": "/srv/sshchan/motd",
                "version": "0.1",
                "name": "sshchan"}

    def __init__(self, cfg_path="/etc/sshchan.conf"):
        self.path = cfg_path
        settings = self.load()

        self.root = settings["rootdir"]
        self.boardlist_path = settings["boardlist_path"]
        self.postnums_path = settings["postnums_path"]
        self.version = settings["version"]
        self.motd = settings["motd_path"]
        self.server_name = settings["name"]
        self.admin = settings["admin"]
        self.salt = settings["salt"]
        self.passwd = settings["password"]

        # Max threads on page.
        self.max_threads = 15 - 1
        # Terminal size.
        self.tty_cols = os.get_terminal_size()[0]
        self.tty_lines = os.get_terminal_size()[1] 
        # Used for laprint() from Display.
        self.lines_printed = 0

    def load(self):
        """Load a JSON configuration file, or return default values."""
        try:
            with open(self.path, 'r') as c:
                config = json.load(c)
            logging.info("Loaded JSON config file.")
            return config
        except FileNotFoundError:
            logging.warning("Config file at %s not found, returning defaults.",
                self.path)
            return Config.defaults

    def save(self, values):
        """Save new or udpated settings to a JSON file."""
        with open(self.path, 'w') as c:
            json.dump(values, c, indent=4)
        logging.info("Dumped new settings into %s.", self.path)
        return True

    def getBoardlist(self):
        """Return the boardlist as a Python dictionary."""
        with open(self.boardlist_path, 'r') as b:
            buf = json.load(b)
        return buf

    def setBoardlist(self, values):
        """Update/create the boardlist with values.

        Boardlist is a standard Python dictionary in the form of
        {"boardname": "description", ...}
        where boardname should be just the name without any slashes
        (but they are not forbidden).
        """
        with open(self.boardlist_path, 'w') as b:
            json.dump(values, b, indent=4)
        logging.info("Updated boardlist file.")
        return True

    def getPostnums(self):
        """Return the postnums file as a Python dictionary."""
        with open(self.postnums_path, 'r') as p:
            buf = json.load(p)
        return buf

    def setPostnums(self, values):
        """Update/create the postnums for board name with value."""
        with open(self.postnums_path, 'w') as p:
            json.dump(values, p, indent=4)
        logging.info("Updated postnums file.")
        return True