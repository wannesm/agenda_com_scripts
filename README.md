# Agenda.com helper scripts

Helper scripts for the [Agenda](https://www.agenda.com) app.

## Usage

### Command line

Requires the `python-xcall` Python package and the `xcall-app`.

Usage:

```
# Get help:
$ ./wm_agenda.py --help
# Create (or open) a note:
$ ./wm_agenda.py note --title "My Note" --project "My Project"
# Open to read list
$ ./wm_agenda.py toread
# Add a new entry
$ ./wm_agenda.py --message "- [ ] Read article at https://www.kuleuven.be/english/research-stories/machine-learning-on-the-pitch" toreadappend
# List of known commands
$ ./wm_agenda.py --list
```

### LaunchBar

To use with [LaunchBar](https://www.obdev.at/products/launchbar/index.html), add an action with the following Python command:

```
#!/usr/local/bin/python3
import sys, wm_agenda
wm_agenda.run_launchbar_todo(sys.argv, action="todo")
```


### Scriptable

There is a `Share with Agenda.js` script to use with the [Scriptable](https://scriptable.app) app for iOS.


## Installation

### Python

- Install the [python-xcall](https://github.com/robwalton/python-xcall) package (which in turn wraps the [xcall](https://github.com/martinfinke/xcall) binary).


## Contact

Wannes Meert  
https://people.cs.kuleuven.be/wannes.meert/

