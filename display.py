"""
Display class handles all the printing, of threads, boards, menus etc.

It uses a special version of print called laprint which stands for
line-aware print. It counts the lines printed to then appropriately
fill the rest of screen with newlines.

Copyright (c) 2015 makos <matmak@protonmail.com>, chibi
"""

import time
import string
import logging
import os

from config import Colors

logging.basicConfig(
        filename="log",
        format="[%(lineno)d]%(asctime)s:%(levelname)s:%(message)s",
        level=logging.DEBUG)

# Instance of Colors class for colored output, e.g. c.RED.
c = Colors()


class Display():

    def __init__(self, config=None, board=None, marker=None):
        assert config is not None, logging.critical(
            "Display.__init__: config is None.")
        self.config = config
        self.board = board
        self.marker = marker
        
        if self.board is None or self.board.name == "":
            self.displayMOTD()
        else:
            self.displayBoard()

    def laprint(self, *args, endc='\n', markup=False):
        """Line-aware print keeps track of number of lines printed."""
        chars = 0
        lines = 0
        msg = ""

        for arg in args:
            msg += str(arg)

        if markup == True and self.marker is not None:
            msg = self.marker.demarkify(msg)

        for c in msg:
            # Stops non-printing characters (such as ANSI codes)
            # from counting towards the chars value.
            if c in string.printable:
                chars += 1
            if c == "\n":
                lines += 1
                chars = 0
            if chars > self.config.tty_cols:
                lines += 1
                chars = 0
            print(c, end='')

        if endc == "\n":
            lines += 1

        print(endc, end="")
        self.config.lines_printed += lines

    def printBoards(self):
        """Print board names and descriptions from boardlist file."""
        for board, desc in self.config.getBoardlist().items():
            self.laprint("/", board, "/\t-\t", desc)

    def layout(self):
        """Fill the rest of screen with newlines."""
        lines_so_far = self.config.lines_printed
        for x in range(lines_so_far, self.config.tty_lines - 1):
            print()
        self.config.lines_printed = 0

    def convert_time(self, stamp):
        """Convert UNIX timestamp to human readable date in local time."""
        return time.strftime('%H:%M:%S %d %b %Y', time.localtime(stamp))

    def displayMOTD(self):
        """Message of the day screen display function."""
        global c  # colors object
        os.system("clear")  # Clear screen.

        self.laprint(
            c.RED, "Welcome to" , c.YELLOW, " sshchan!\n===========",
            c.RED, "========", c.BLACK)
        self.laprint(
            c.GREEN, "SERVER:\t", c.BLACK, self.config.server_name)
        self.laprint(c.GREEN, "MOTD:", c.BLACK)

        # Read MOTD file.
        try:
            motd = open(self.config.motd, 'r')
            self.laprint(motd.read())
        except FileNotFoundError:
            self.laprint("---sshchan! woo!---")

        self.laprint(c.GREEN, "BOARDS:", c.BLACK)
        self.laprint("This server has the following boards:")
        self.printBoards()
        self.layout()

    def displayBoard(self, page=1):
        """Parses and prints threads in the board index.
        Board index JSON layout:
        [
         ['thread id', 'subject', 
          ['unix timestamp', 'post no', 'post'] <--- OP
          ['unix timestamp', 'post no', 'post'] <--- reply #1
          ...
         ]
         ['thread_id', 'subject', ...]
        ]
        """
        global c
        assert self.board is not None, logging.critical(
            "Display.displayBoard(): board is None.")
        os.system("clear")  # Clear screen.
        lines_printed = 0
        index = self.board.getIndex()

        # First check if we even have a valid index.
        if type(index) != list or len(index) == 0:
            self.laprint(c.bBLACK, "Board is empty.", c.BLACK)
            self.layout()
            return False

        # Those two lines compute what threads to show on specified page.
        max_on_page = self.config.max_threads * page
        i = self.config.max_threads * (page - 1)

        for thread in index[i:]:
            if i < max_on_page:
                date = self.convert_time(int(thread[2][0]))

        # NOTE:
        # Board display functions should use laprint() instead of print()
        # laprint() keeps track of the number of lines printed so things
        # can be displayed properly.
        # There are two differences between laprint() and print():
        # the ending character is called 'endc' in laprint
        # e.g. laprint('hello', endc='').
                self.laprint(
                    c.GREEN, date, c.BLACK, ' No.',
                    str(thread[0]), endc = ' ')
                self.laprint(c.bRED, thread[1], c.BLACK)
                self.laprint(thread[2][2], markup=True)
                if len(thread) > 3:
                    self.laprint(
                        c.GREEN, str(len(thread) - 3),
                        " posts hidden. Type v ", str(thread[0]),
                        " to view.", c.BLACK)
                self.laprint('--------')

                i += 1
        self.laprint(c.BLUE, 'Page ', str(page), c.BLACK)

        # Fill the rest of the page with newlines.
        self.layout()
        
    def displayThread(self, thread_id):
        global c
        assert self.board is not None, logging.critical(
            "Display.displayBoard(): board is None.")
        os.system("clear")  # Clear screen.
        index = self.board.getIndex()

        for thread in index:
            if thread[0] == int(thread_id):
                date = self.convert_time(int(thread[2][0]))
                # Print OP first.
                self.laprint(
                    c.GREEN, date, c.BLACK, ' No.',
                    str(thread[0]), endc=' ')
                self.laprint(c.bRED, thread[1], c.BLACK)
                self.laprint(thread[2][2], '\n', markup=True)

                # Then replies, if there are any.
                if len(thread) > 3:
                    for reply in thread[3:]:
                        date = self.convert_time(int(reply[0]))
                        self.laprint(
                            c.GREEN, date, c.BLACK, ' No.', str(reply[1]))
                        self.laprint(reply[2], '\n', markup=True)
        self.layout()

    def postMenu(self, thread_id=-1):
        buf = ""
        print("Post text: (make an empty line to stop editing)")

        while True:
            text = input()
            if not text:
                break
            buf += text + "\n"
        buf = buf.rstrip("\n")  # Get rid of extra newline at the end.

        if thread_id == -1:
            subject = input("Thread subject: ")
            opt = input("Do you want to post that? y/n ")
            if opt == 'y':
                if self.board.addPost(buf, subject):
                    print(c.GREEN, "Post succesful!", c.BLACK)
                else:
                    print(c.RED, "Posting failed!", c.BLACK)
            else:
                print("Post scrapped.")
        else:
            opt = input("Do you want to post that? y/n ")
            if opt == 'y':
                if self.board.addPost(buf, thread_id=thread_id):
                    print(c.GREEN, "Post succesful!", c.BLACK)
                else:
                    print(c.RED, "Posting failed!", c.BLACK)
            else:
                print("Post scrapped.")
