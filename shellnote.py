#!/usr/bin/python

import argparse
import os
import sys
from time import strftime
from re import search
import yaml

homedir = os.path.expanduser("~")
configfile = "config.py"
configpath = os.path.join(homedir, ".config", "shellnote", configfile)
version_str = "0.1"

if os.path.exists(configpath):
    exec(open(configpath).read())
else:
    logdir = homedir
    logfile = "shellnote.txt"
    logpath = os.path.join(logdir, logfile)
    delim = "\t"

def add_note(text, quiet=True):
    entry_date = strftime("%Y-%m-%d")
    entry_time = strftime("%H:%M:%S")
    entry_id = hash(entry_date+entry_time) 
    entry_tags = None
    entry = [{"id": entry_id, "date": entry_date, "time": entry_time, 
         "tags": entry_tags, "note": text}]
    entry = yaml.dump(entry, sort_keys=False) # make yaml format
    with open(logpath, "a") as file:
        file.write(entry + "\n")
    if quiet:
        print(f"Added entry to {logpath}")

def search_note(search_term, txt):
    txt_split = txt.splitlines()
    indexes = []
    for i in range(len(txt_split)):
        match = search(search_term, txt_split[i])
        if match:
            indexes.append(i)
    result = [txt_split[i] for i in indexes]
    for i in range(len(result)):
        print(result[i])

def launch_editor():
    editor = os.environ.get("EDITOR")
    if editor is None:
        if "linux" in sys.platform:
            editor = "vi"
        elif sys.platform == "darwin":
            editor = "nano"
        elif sys.platorm == "win32":
            editor = "notepad.exe"
    os.system(editor + " " + logpath)

def main():
    ap = argparse.ArgumentParser(prog="shellnote",
            description="shellnote: easy note-taking on the command line.")
    
    ## arguments
    ap.add_argument("-a", "--add", help="add note", action="store",
            metavar="NOTE")
    ap.add_argument("-e", "--edit", 
            help="edit current entries in your text editor", 
            action="store_true")
    ap.add_argument("-i", "--input", help="add note by input prompt", 
            action="store_true")
    ap.add_argument("-p", "--print", help="print entries", action="store_true")
    ap.add_argument("-s", "--search", help="search entries", action="store",
            metavar="TERM")
    ap.add_argument("-v", "--version", action="version", version=version_str)
    ap.add_argument("-q", "--quiet", help="suppress output", 
            action="store_false")
    
    args = ap.parse_args()

    if args.add:
        add_note(args.add, args.quiet)
    
    if args.print:
        with open(logpath, "r") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        for i in range(len(data)):
            print(data[i]['date'] + " " + data[i]['time'][0:5] + \
                    '\t' + data[i]['note'])

    if args.edit:
        launch_editor()
    
    if args.input:
        note = input("Note: ")
        entry = make_yaml_entry(note)
        write_entry(entry)
        if args.quiet:
            print(f"Added entry to {logpath}")

    if args.search:
        with open(logpath, "r") as file:
            txt = file.read()
        search_note(args.search, txt)
    
    # if no arguments provided, launch curses tui
    if not any(vars(args).values()):
        exec(open("shellnote-tui.py").read())

if __name__ == "__main__":
    main()
