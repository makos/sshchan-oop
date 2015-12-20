sshchan-setup
===

Usage
---
Initialisation (setting up sshchan for the first time):
`python3 setup.py`

Administration (changing configuration, adding/removing boards, etc.):
`python3 sshchan.py`
Then, in commandline:
`admin`
Enter the password.

Administration
---
This can be done from the `sshchan.py` module by submitting `admin` command.

### `add [board name] [board description]`
Adds the board to your boardlist and creates the needed directories and files. NOTE: Every character after the board name will become part of the description. There is no need to add inverted commas.
e.g.
	add a Animu and Mango
	add tech Technology
etc.

### `del [board name]`
Removes the specified board name (without slashes) from the boardlist.

### `rename [board name] [new description]`
Changes the specified board's description to [new description]. 

### `config [config option] [value]`
Sets the value of [config option] to [value] in `/etc/sshchan.conf`. See `docs/config.md` for a list of config options.

### `list | ls`
Lists all the current boards.
