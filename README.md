sshchan-oop
=======

This is a fork of sshchan from http://neetco.de/chibi/sshchan, originally developed by chibi with my contributions. I wanted to refactor the code into an object-oriented approach, and so this repository was created.

A textboard environment implemented in Python. At the moment it is a script meant to be run server-side by a user connecting to that server using ssh. It hopes to be configurable and secure.

Status / Warning
---

sshchan is not usable as of now. Do not run the scripts, especially `setup.sh` unless you are a developer or very curious and willing to tolerate bugs and mishaps.

### gui status

We were working on a curses gui in `gui.py` but there have been problems and development on that has temporarily stopped. If you want to try out sshchan, run `sshchan.py` instead.

How to Install / Dependencies
---

	git clone http://neetco.de/chibi/sshchan.git sshchan
	cd sshchan
	python3 setup.py
That should set up the basic chan for you. From there, read the documentation `docs/setup.md` for more admin stuff.

Scripts
---
There are several scripts in sshchan:
* `sshchan.py` is the user script for reading from/posting to the chan.
* `setup.py` is the script the admin runs to set up a new chan.

How to use
---

When it becomes usable, sshchan will be a full script that emulates a textboard based on the files provided by the server, which acts as the chan operator. The main usage scenario is that users log into an anonymous user account on the chan operator's ssh server, which forces them to run the script with this line in your `/etc/ssh/sshd_config`:
	Match User anonymous
	ForceCommand 'python3 sshchan.py'
The script then provides the environment of a textboard so that users can make threads and posts from within the script.

Configuration
---

The role of the server admin is paramount. He decides the boards and all the configuration options (see more about configuration in `docs/config.md`) which control the behaviour of the script. Here are the configuration files:
* `/etc/sshchan.conf` is the default one. sshchan reads this at startup, unless specified otherwise. To load a custom config, provide the path as first argument when running sshchan.py (e.g. `python3 sshchan.py /path/to/config`)
* `[root]/boardlist` is the list of boards and their topic-titles, where `[root]` is the root directory of the chan.

The root directory of the chan can be set by the `rootdir` config option in `/etc/sshchan.conf`.

Roadmap
---

* Decide upon and implement markup language for threads
* Ascii CAPTCHAs
* Secure admin authentication