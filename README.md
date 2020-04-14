# Agenda.com helper scripts

Helper scripts for [Agenda](https://www.agenda.com)

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

To use with [LaunchBar](https://www.obdev.at/products/launchbar/index.html):

```
#!/usr/local/bin/python3
import sys, wm_agenda
wm_agenda.run_launchbar_todo(sys.argv, action="todo")
```


### Scriptable

There is a `Share with Agenda.js` script to use with `Scriptable`.


## Contact

Wannes Meert  
https://people.cs.kuleuven.be/wannes.meert/

