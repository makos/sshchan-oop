#!/usr/bin/env python3
"""
Main file of sshchan, it ties up other files together.
User interacts with the chan through the use of a commandline.
Any user can create new threads, reply to other posts and freely browse
the boards. Only admins can add boards.

Copyright (c) 2015
makos <https://github.com/makos>, chibi <http://neetco.de/chibi>
under GNU GPL v3, see LICENSE for details
"""

import logging
import sys
import os
import hashlib
import getpass
# sshchan imports
import admin
import config
from boards import Board
from chan_mark import Marker
from display import Display


def authenticate(display, config, password):
    """Authentication function for admin cmdline."""
    salt = bytes.fromhex(config.salt)
    pwd = bytes.fromhex(config.passwd)
    user = config.admin
    password = bytes(password, "utf-8")
    sha = hashlib.sha256()

    if user == getpass.getuser():
        sha.update(salt + password)
        if sha.digest() == pwd:
            return True
        else:
            return False


def print_help(display, marker):
    display.laprint(
"[sshchan.py] help\n", 
c.GREEN,"exit", c.BLACK, " - quit sshchan\n", 

c.GREEN,"help | h", c.BLACK, " - print this message\n",

c.GREEN,"list | ls", c.BLACK, " - list the boards on the server\n",

c.GREEN, "board | b [name] [page]", c.BLACK, " - display board contents, \
optionally specify a page\n", 

c.GREEN, "page | p [integer]", c.BLACK, " - when in board view, use this to \
browse pages\n", 

c.GREEN, "reply | re [integer]", c.BLACK, " - reply to a thread specified by \
integer ID\n\tor make a new thread on specified board \
(not needed if in board view)\n", 

c.GREEN, "view | v [integer]", c.BLACK, " - show replies to a thread specified\
 by integer ID\n", 

c.GREEN, "refresh | r", c.BLACK, " - refresh current board view\n", 

c.GREEN, "motd", c.BLACK, " - show MOTD", 

c.YELLOW, "\n\nMarkup help\n", c.BLACK,
"Wrap your text in following characters to style the post:\n",
"==reverse video==\t", marker.demarkify("==reverse video==\n"),
"'''bold text'''\t\t", marker.demarkify("'''bold text'''\n"))
    display.layout()


def cmdline(cfg, display, board, marker, c):
    """Receives and interprets user commands."""
    if board.name == '':
        cmd = str(input(c.BLUE + "sshchan/> " + c.BLACK))
    else:
        cmd = str(input(c.BLUE + "sshchan/" + board.name + "/> " + c.BLACK))
    cmd_argv = cmd.split()

    # If there is no input. Avoids IndexError in command parsing.
    if len(cmd_argv) == 0:
        print_help()
        return False

    if cmd_argv[0] in ("board", "b"):
        if len(cmd_argv) > 1:
            if cmd_argv[1] in cfg.getBoardlist().keys():
                board.name = cmd_argv[1]
                print("board.name:", board.name)
                
                if len(cmd_argv) > 2:
                    display.displayBoard(int(cmd_argv[2]))
                else:
                    display.displayBoard()
            else:
                print(c.RED, "Board {} does not exist.".format(cmd_argv[1]),
                    c.BLACK)
        else:
            print("ERROR: Please specify a board")
            return False
        return True

    elif cmd_argv[0] == "exit":
        sys.exit(0)

    elif cmd_argv[0] in ("help", "h"):
        print_help(display, marker)
        return True

    elif cmd_argv[0] in ("list", "ls"):
        display.printBoards()
        display.layout()
        return True

    # Following allows to browse board pages just by typing a number.
    elif cmd_argv[0] in ("page", "p"):
        if board.name != '' and len(cmd_argv) > 1:
            if cmd_argv[1].isalnum():
                display.displayBoard(int(cmd_argv[1]))

    elif cmd_argv[0] in ("reply", "re"):
        if board.name != '':
            if len(cmd_argv) > 1:
                # If thread ID was specified.
                display.postMenu(int(cmd_argv[1]))
            else:
                # Post new thread.
                display.postMenu()

    elif cmd_argv[0] in ("view", "v"):
        if board.name != '' and len(cmd_argv) > 1:
            if cmd_argv[1].isdigit():
                display.displayThread(cmd_argv[1])

    elif cmd_argv[0] in ("refresh", "r"):
        if board.name != '':
            display.displayBoard()

    elif cmd_argv[0] == "motd":
        display.displayMOTD()

    elif cmd_argv[0] == "admin":
        passwd = getpass.getpass("Password: ")
        if authenticate(display, cfg, passwd):
            admin.cmdline(cfg, display, board, c)

    else:
        print("ERROR: Command " + cmd_argv[0] + " not found.")
        print_help(display, marker)
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            cfg = config.Config(sys.argv[1])
        else:
            print("Invalid configuration file path.")
            sys.exit(1)
    else:
        cfg = config.Config()
    marker = Marker()
    board = Board(config=cfg)
    display = Display(config=cfg, board=board, marker=marker)
    # terminal colors object
    c = config.Colors()

    logging.basicConfig(
        filename="log",
        format="[%(lineno)d]%(asctime)s:%(levelname)s:%(message)s",
        level=logging.DEBUG)
    
    while True:
        cmdline(cfg, display, board, marker, c)