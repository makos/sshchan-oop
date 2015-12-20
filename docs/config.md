Configuration
===

This is a list of configuration options for the various config files involved with sshchan.

`/etc/sshchan.conf`
---
### `rootdir`
The root directory of the chan, i.e. where all the boards lie within. This is normally set during initialisation (see `docs/setup.md`).

### `boardlist_path`
The boardlist file path. It's usually inside of `rootdir`, but it can be changed to any path. NOTE: Boardlist is a file, not a directory.

### `postnums_path`
Postnums file path. Postnums is a file that contains the information about post numbers on a given board. It is automatically updated every time a new post is made.

### `name`
The name of the server. This is a string displayed to users at the top of their window when they first connect. It can be anything: an IP, a hostname, your name or the name of your secret society.

### `motd_path`
The path to the file whose contents will be displayed as the Message of the Day. This appears at the top of the window when users first connect.

### `version`
The version of sshchan that you are using. This is set during initialisation. It would be wise not to change it.
