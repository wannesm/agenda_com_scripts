#!/usr/bin/env python3
# encoding: utf-8
"""
wm_agenda.py

Copyright (c) 2019 Wannes Meert. All rights reserved.
"""

import sys
import argparse
import logging
import os
from pathlib import Path
import datetime
from dataclasses import dataclass
import subprocess as sp

logger = logging.getLogger(__name__)
here = Path(os.path.realpath(__file__)).parent
sys.path.append(str(here / "python-xcall"))
import xcall



@dataclass
class Arguments:
    title: str = None
    project: str = None
    message: str = None
    date: str = None
    week: int = None
    year: int = None

    def __post_init__(self):
        if self.date is None:
            if self.week is None or self.year is None:
                now = datetime.date.today()
                year, week, _ = now.isocalendar()
                if self.year is None:
                    self.year = year
                if self.week is None:
                    self.week = week
            self.date = self.monday_str()


    def previous_week(self):
        if self.week == 1:
            week = 52
            year = year - 1
        else:
            week = self.week - 1
            year = self.year
        return Arguments(week=week, year=year)


    def week_str(self):
        weekstr = f"{self.year}W{self.week:02}"
        return weekstr


    def monday_str(self):
        weekstr = self.week_str()
        # monday = datetime.datetime.strptime(weekstr + '-1', "%YW%W-%w")
        week2str = f"{self.year}W{self.week-1}"
        monday = datetime.datetime.strptime(week2str + '-1', "%YW%W-%w")
        mondaystr = monday.strftime("%Y-%m-%d")
        return weekstr, mondaystr



# OPEN ####################################################################

def open_agenda(args):
    sp.run(["open", "-a", "agenda"])
    # try:
    #     resp = xcall.xcall('agenda', '')
    # except xcall.XCallbackError as err:
    #     logger.error(err)


def print_currentweek(args):
    weekstr, mondaystr = args.monday_str()
    print(f"{weekstr}  --  Monday={mondaystr}")


def note_check_args(args, create=False):
    if args.title is None:
        logger.error(f"A title is required to open a note")
        sys.exit(1)
    if create:
        if args.project is None:
            logger.error(f"A project is required to create a note")
            sys.exit(1)


def note_open(args):
    note_check_args(args)
    parameters = {
        'title': args.title,
    }
    if args.project is not None:
        parameters['project-title'] = args.project
    try:
        resp = xcall.xcall('agenda', 'open-note', parameters)
    except xcall.XCallbackError as err:
        logger.debug(err)
        note_create(args)
        return
    logger.debug(resp)


def note_create(args):
    note_check_args(args, create=True)
    parameters = {
        'title': args.title,
        'on-the-agenda': 'false'
    }
    if args.date is not None:
        parameters['date'] = args.date
    if args.project is not None:
        parameters['project-title'] = args.project
    if args.message is not None and args.message != "":
        parameters["text"] = f"{args.message}\n"
    try:
        resp = xcall.xcall('agenda', 'create-note', parameters)
    except xcall.XCallbackError as err:
        logger.error(err)
        return
    logger.debug(resp)


def note_append(args):
    note_check_args(args)
    parameters = {
        'title': args.title,
    }
    if args.project is not None:
        parameters['project-title'] = args.project
    if args.message is not None and args.message != "":
        parameters["text"] = f"{args.message}\n"
    else:
        return
    try:
        resp = xcall.xcall('agenda', 'append-to-note', parameters)
    except xcall.XCallbackError as err:
        logger.error(err)
        note_create(args)
        return
    logger.debug(resp)


# TO DO ###################################################################

def weeklytodo_run(**kwargs):
    args = Arguments(**kwargs)
    if kwargs.get("message", None) is None:
        weeklytodo(args)
    else:
        weeklytodo_append(args)


def weeklytodo(args):
    logger.debug("Call weeklytodo")
    weekstr = args.week_str()
    try:
        resp = xcall.xcall(
            'agenda',
            'open-note',
            {
                'title': "Todo " + weekstr,
                'project-title': 'Todo'
            })
    except xcall.XCallbackError as err:
        logger.debug(err)
        weeklytodo_create(args)
        return
    logger.debug(resp)


def weeklytodo_create(args):
    logger.debug("Call weeklytoreadcreate")
    weekstr, mondaystr = args.monday_str()
    parameters = {
        'title': "Todo " + weekstr,
        'project-title': 'Todo',
        'date': mondaystr,
        'on-the-agenda': 'false'
    }
    text = "#todo\n\n# This week\n- [ ] ...\n\n\n# Later\n\n\n# Done\n\n\n# To Handle\n"
    if args.message is not None and args.message != "":
        text += f"- [ ] {args.message}\n"
    parameters["text"] = text
    try:
        resp = xcall.xcall(
            'agenda',
            'create-note',
            parameters)
    except xcall.XCallbackError as err:
        logger.error(err)
        return
    logger.debug(resp)


def weeklytodo_append(args):
    logger.debug("Call weeklytodoappend")
    weekstr, mondaystr = args.monday_str()
    parameters = {
        'title': "Todo " + weekstr,
        'project-title': 'Todo'
    }
    if args.message is not None and args.message != "":
        parameters["text"] = f"- [ ] {args.message}\n"
    else:
        return
    try:
        resp = xcall.xcall(
            'agenda',
            'append-to-note',
            parameters)
    except xcall.XCallbackError as err:
        logger.error(err)
        weeklytodo_create(args)
        return
    logger.debug(resp)


def weeklytodo_parse(args):
    logger.debug("Parsing todo")
    weekstr = args.week_str()
    prevweekstr = args.previous_week().week_str()
    print("No x-callback-url for reading a note (yet) in Agenda")


# TO READ #################################################################

def weeklytoread_run(**kwargs):
    args = Arguments(**kwargs)
    if kwargs.get("message", None) is None:
        weeklytoread(args)
    else:
        weeklytoread_append(args)


def weeklytoread(args):
    logger.debug("Call weeklytoread")
    weekstr = args.week_str()
    try:
        resp = xcall.xcall(
            'agenda',
            'open-note',
            {
                'title': "To Read " + weekstr,
                'project-title': 'To Read'
            })
    except xcall.XCallbackError as err:
        logger.debug(err)
        weeklytoread_create(args)
        return
    logger.debug(resp)


def weeklytoread_create(args):
    logger.debug("Call weeklytoreadcreate")
    weekstr, mondaystr = args.monday_str()
    parameters = {
        'title': "To Read " + weekstr,
        'project-title': 'To Read',
        'date': mondaystr,
        'on-the-agenda': 'false'
    }
    if args.message is not None and args.message != "":
        parameters["text"] = f"- [ ] {args.message}\n"
    try:
        resp = xcall.xcall(
            'agenda',
            'create-note',
            parameters)
    except xcall.XCallbackError as err:
        logger.error(err)
        return
    logger.debug(resp)


def weeklytoread_append(args):
    logger.debug("Call weeklytoreadappend")
    weekstr, mondaystr = args.monday_str()
    parameters = {
        'title': "To Read " + weekstr,
        'project-title': 'To Read'
    }
    if args.message is not None and args.message != "":
        parameters["text"] = f"- [ ] {args.message}\n"
    else:
        return
    try:
        resp = xcall.xcall(
            'agenda',
            'append-to-note',
            parameters)
    except xcall.XCallbackError as err:
        logger.error(err)
        weeklytoread_create(args)
        return
    logger.debug(resp)


# LAUNCHBAR ##################################################################

def run_launchbar(argv, action="todo"):
    """
    This function can be called from a LaunchBar script. For example, in
    the Action Editor create a new Action with as default script:

    ```
    #!/usr/local/bin/python3
    import sys, wm_agenda
    wm_agenda.run_launchbar_todo(sys.argv, action="todo")
    ```

    And with only the checkbox "Accept string argument" checked.

    Params:
    args - Arguments passed from launchbar
    action - Type of action: "todo" or "toread"
    """
    import json
    items = []

    item = {}
    item['title'] = str(len(argv) - 1) + ' arguments passed'
    items.append(item)

    if action == "todo":
        fn = weeklytodo_run
    elif action  == "toread":
        fn = weeklytoread_run
    else:
        logger.error(f"Unknown action: {action}")
        return

    if len(argv) == 1:
        fn()
    elif len(argv) == 2:
        fn(message=argv[1])

    # Note: The first argument is the script's path
    for arg in argv[1:]:
        item = {}
        item['title'] = 'Argument: ' + arg
        items.append(item)

    print(json.dumps(items))


# CLI ########################################################################

commands = {
    "note": note_open,
    "open": open_agenda,
    "toread": weeklytoread,
    "toreadcreate": weeklytoread_create,
    "toreadappend": weeklytoread_append,
    "todo": weeklytodo,
    "todocreate": weeklytodo_create,
    "todoappend": weeklytodo_append,
    "todoparse": weeklytodo_parse,
    "curweek": print_currentweek
}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Agenda scripts')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Verbose output')
    parser.add_argument('--quiet', '-q', action='count', default=0, help='Quiet output')
    # parser.add_argument('--flag', '-f', action='store_true', help='Flag help')
    # parser.add_argument('--output', '-o', required=True, help='Output file')
    # parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    # parser.add_argument('--type', '-t', choices=['toread', 'todo'], default='toread')
    parser.add_argument('--week', '-w', type=int, help='Week')
    parser.add_argument('--year', '-y', type=int, help='Year')
    parser.add_argument('--message', '-m', help='Message to add to note/todo/toread')
    parser.add_argument('--title', '-t', help='Note title')
    parser.add_argument('--project', '-p', help='Project title')
    parser.add_argument('--date', '-d', help='Note date, expected format is "YYYY-mm-dd"')
    parser.add_argument('--list', '-l', action='store_true', help='List possible commands')
    parser.add_argument('cmd', nargs='*', help='List of commands: '+", ".join(commands.keys()))
    args = parser.parse_args(argv)

    logger.setLevel(max(logging.INFO - 10 * (args.verbose - args.quiet), logging.DEBUG))
    logger.addHandler(logging.StreamHandler(sys.stdout))
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"Here: {here}")
        xcall.enable_verbose_logging()

    if args.list:
        for key, val in commands.items():
            print(key)
        return

    if args.cmd is None or len(args.cmd) == 0:
        # if args.message is not None and args.message != "":
        #     cmd = ['weeklytoreadappend']
        # else:
        cmd = ['open']
    else:
        cmd = args.cmd
    args = Arguments(title=args.title, message=args.message,
                     project=args.project, date=args.date,
                     week=args.week, year=args.year)

    for key, fn in commands.items():
        if key in cmd:
            commands[key](args)


if __name__ == "__main__":
    sys.exit(main())

