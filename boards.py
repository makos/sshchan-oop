"""
Board class allows operation on a board, like posting, creating threads etc.
If it is instantiated with name parameter that isn't found in boardlist
file, the board and relevant files (index, postnums) are automatically created
and updated.

Copyright (c) 2015
makos <https://github.com/makos>, chibi <http://neetco.de/chibi>
under GNU GPL v3, see LICENSE for details
"""

import json
import os
import logging
import shutil
import time

logging.basicConfig(
        filename="log",
        format="[%(lineno)d]%(asctime)s:%(levelname)s:%(message)s",
        level=logging.DEBUG)


class Board():
    """Class holding data of the currently selected board."""

    def __init__(self, name='', desc='', config=None):
        assert config is not None, logging.critical(
            "Board.__init__: config is None")
        # Configuration object used to read / write config values.
        self.config = config            

        self._name = name.lower()
        self._desc = desc
        self.path = os.path.join(self.config.root, "boards", self._name)
        self.index_path = os.path.join(self.path, "index")
        self.boardlist_path = self.config.boardlist_path

        if self.addBoard():
            logging.info(
                'Board "/%s/ - %s" added succesfully.', self._name, self._desc)

    def __eq__(self, other):
        """Equality (==) operator overload method."""
        if self._name == other.name and self._desc == other.desc:
            return True
        else:
            return False

    def addBoard(self):
        """Adds board to the boardlist and creates all relevant files.

        If the Board class is instantiated with a name parameter that
        isn't present in the current boardlist, the board is
        automatically added and all directories and files are also
        created.
        """

        if self._name in self.config.getBoardlist().keys() \
                or self._name == '':
            return False
        # Add the board to boardlist.
        buf = self.config.getBoardlist()
        buf[self._name] = self._desc
        self.config.setBoardlist(buf)
        # Create the board directory.
        try:
            os.makedirs(self.path)
        except OSError as e:
            logging.error("Board.addBoard(): %s", e)
        # Create the index file.
        self.setIndex([])
        # Edit postnums.
        postn = self.config.getPostnums()
        postn[self._name] = 0
        self.config.setPostnums(postn)

        return True

    def delBoard(self):
        if self._name != "":
            os.remove(self.index_path)
            os.rmdir(self.path)
            boardlist = self.config.getBoardlist()
            del boardlist[self._name]
            self.config.setBoardlist(boardlist)
            logging.info("Board %s deleted succesfully.", self._name)
            self._name = ""
            self.desc = ""
            self.path = ""
            self.index_path = ""
            return True
        else:
            return False

    def getIndex(self):
        """Returns a list containing the board's index."""
        with open(self.index_path, 'r') as i:
            buf = json.load(i)
        return buf

    def setIndex(self, values):
        """Update the board's index with new values."""
        with open(self.index_path, 'w') as i:
            json.dump(values, i, indent=4)
        return True

    @property
    def name(self):
        """Property method for getting name of the board."""
        return self._name

    @name.setter
    def name(self, value):
        """Property setter method for setting name of the board.

        Assignments like board.name = 'b' should ONLY be used
        if the board already exists. If you want to rename the
        board and change all relevant files and directories,
        use the rename() method. If you want to create a board,
        use the addBoard() method."""
        self._name = value
        self.path = os.path.join(self.config.root, "boards", self._name)
        self.index_path = os.path.join(self.path, "index")
        self.boardlist_path = self.config.boardlist_path

    @property
    def desc(self):
        """Getter for description field."""
        return self._desc

    @desc.setter
    def desc(self, value):
        """Setter for description field."""
        self._desc = value

    def rename(self, name, desc=""):
        """Rename the board, and change boardlist and index directory."""
        if desc == "":
            desc = self._desc
        if self._name in self.config.getBoardlist().keys():
            # Change boardlist.
            buf = self.config.getBoardlist()
            buf[name] = desc
            del buf[self._name]
            self.config.setBoardlist(buf)
            # Change directories.
            try:
                new_path = os.path.join(self.config.root, '/boards/' + name)
                os.makedirs(new_path)
                # Copy index file.
                shutil.copy(self.index_path, new_path)
                os.remove(self.index_path)
                os.removedirs(self.path)
            except OSError:
                logging.error("Board.addBoard: %s", e)
                return False
            # rRe-point the class fields to new values.
            self._name = name
            self._desc = desc
            self.path = new_path
            self.index_path = os.path.join(new_path, '/index')

            return True

    def addPost(self, post_text, subject="", thread_id=-1):
        """Posts a thread or a reply to a thread.
        
        If thread_id is not specified (i.e. = -1), a new thread
        is created. Posting depends on the file (rootdir)/postnums
        which has the following JSON structure:
        [{'a': max_post_no}, {'b': max_post_no}, ...]
        where max_post_no is the current highest post number.
        
        Thread / post format is as follows:
        index page is a standard Python list, where
        index[0] is the first thread with ID 1,
            index[1] is the second thread etc.
        index[n][0] is the ID of n-th thread
        index[n][1] is the subject
        index[n][2] is the first reply, where
            index[n][2][0] is the Unix timestamp
            index[n][2][1] is the ID (post number)
            index[n][2][2] is the text (body)
        index[n][k], where k > 1, is the k-th reply to n-th thread
        """
        index_page = self.getIndex()
     
        postnums = self.config.getPostnums()
        max_post_no = postnums[self._name]
        timestamp = int(time.time())

        if thread_id == -1:
            # Add a new thread.
            index_page.append(
                [max_post_no + 1, subject,
                [timestamp, max_post_no + 1, post_text]])
            self.setIndex(index_page)
            postnums[self._name] += 1
            self.config.setPostnums(postnums)
            return True
        else:
            # Add reply to an existing thread.
            thread_id = abs(thread_id)
            # Maybe get a better search algorithm?
            for x in range(0, len(index_page)):
                thread = index_page[x]
                cur_thread_id = thread[0]

                if cur_thread_id == thread_id:
                    thread.append([timestamp, max_post_no + 1, post_text])
                    self.setIndex(index_page)
                    postnums[self._name] += 1
                    self.config.setPostnums(postnums)
                    return True
        return False  # If posting fails.