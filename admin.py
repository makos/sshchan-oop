#-*- coding: utf-8 -*-
# sshchan admin/config panel
from sys import exit

def cmdline(cfg, display, board, c):
    print(c.YELLOW, "sshchan-admin", c.BLACK)
    while True:
        cmd = str(input(c.BLUE + "sshchan/" + c.RED + "ADMIN" + c.BLUE + "> " \
            + c.BLACK))
        cmd_argv = cmd.split()

        if cmd_argv[0] in ("help", "h"):
            print(
c.GREEN, "Available commands:\n\
 add [name] [description] - ",  c.BLACK,
"adds a board with [name] and [description]\n\
don't use slashes, they're added automatically.\n", 

c.GREEN, "del [name] - ", c.BLACK, "delete board [name]\n", 

c.GREEN, "list|ls - ", c.BLACK, "lists boards\n", 

c.GREEN, "rename [name] [new description] - ", c.BLACK,
"changes the description of board [name] to [new description]\n", 

c.GREEN, "exit - ", c.BLACK, "exits sshchan-admin")

        elif cmd_argv[0] in ("list", "ls"):
            display.printBoards()

        elif cmd_argv[0] == "add":
            if len(cmd_argv) > 2:
                description = ''
                board.name = cmd_argv[1]
                for word in cmd_argv[2:]:
                    description += word + ' '
                board.desc = description.rstrip()
                if board.addBoard():
                    print(c.GREEN, "Board /", board.name, "/ added \
succesfully.", c.BLACK)
                else:
                    print(c.RED, "There was an error creating the board.",
                        c.BLACK)
            else:
                print(c.RED, "Please provide board name and description \
separated by whitespace.", c.BLACK)

        elif cmd_argv[0] == "del":
            if len(cmd_argv) > 1:
                # board = cmd_argv[1]
                board.name = cmd_argv[1]
                answer = str(input("Are you sure you want to delete \
board /" + board.name + "/? (y/n): "))
                if answer == "y":
                    if board.delBoard():
                        print(c.GREEN, "Board deleted succesfully.", c.BLACK)
                    else:
                        print(c.RED, "Board deletion failed.", c.BLACK)
                else:
                    print(c.GREEN, "No action taken.", c.BLACK)
            else:
                print(c.RED, "Please specify the board you want to delete.",
                    c.BLACK)

        elif cmd_argv[0] == "rename":
            if len(cmd_argv) > 2:
                newname = cmd_argv[1]
                newdesc = ''
                for word in cmd_argv[2:]:
                    newdesc += word + ' ' 
                if board.rename(newname, newdesc):
                    print(c.GREEN, "Board renamed successfully.", c.BLACK)
                else:
                    print(c.RED, "Failed to rename board.", c.BLACK)
            else:
                print(c.RED, "Please specify the board and its new description.",
                    c.BLACK)

        elif cmd_argv[0] == "exit":
            break

        else:
            print(c.RED, "Command", cmd_argv[0], "not found.", c.BLACK)