#!/usr/bin/python

from argparse import ArgumentParser
import os
from time import strftime
from re import search
import yaml

homedir = os.getenv("HOME")
configfile = ".shellnote2rc"
configpath = homedir+"/"+configfile

if os.path.exists(configpath):
    exec(open(configpath).read())
else:
    logdir = homedir
    logfile = "shellnote2.txt"
    logpath = logdir + "/" + logfile
    delim = "\t"
    
version_str = "0.1"

def make_yaml_entry(note):
     entry_date = strftime("%Y-%m-%d")
     entry_time = strftime("%H:%M:%S")
     entry_id = hash(entry_date+entry_time) 
     entry_tags = None
     entry = [{"id": entry_id, "date": entry_date, "time": entry_time, 
         "tags": entry_tags, "note": note}]
     yaml_entry = yaml.dump(entry, sort_keys=False)
     return yaml_entry

def write_entry(entry):
    with open(logpath, "a") as file:
        file.write(entry + "\n")

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

def main():
    ap = ArgumentParser(prog="shellnote2", description="shellnote2: easy note-taking on the command line.")
    
    ## arguments
    ap.add_argument("-a", "--add", help="add note", action="store", metavar="NOTE")
    ap.add_argument("-e", "--edit", help="edit current entries in your text editor", action="store_true")
    ap.add_argument("-i", "--input", help="add note by input prompt", action="store_true")
    ap.add_argument("-p", "--print", help="print entries", action="store_true")
    ap.add_argument("-s", "--search", help="search entries", action="store", metavar="TERM")
    ap.add_argument("-v", "--version", action="version", version=version_str)
    ap.add_argument("-q", "--quiet", help="suppress output", action="store_true")
    
    args = ap.parse_args()
    
    if args.add:
        entry = make_yaml_entry(args.add)
        write_entry(entry)
        if not args.quiet:
            print(f"Added entry to {logpath}")
    
    if args.print:
        with open(logpath, "r") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        for i in range(len(data)):
            print(data[i]['date'] + " " + data[i]['time'][0:5] + '\t' + data[i]['note'])

    if args.edit:
        if "EDITOR" in os.environ:
            os.system(f"$EDITOR {logpath}")
        else:
            os.system(f"vim {logpath}")
    
    if args.input:
        note = input("Note: ")
        entry = make_yaml_entry(note)
        write_entry(entry)
        if not args.quiet:
            print(f"Added entry to {logpath}")

    if args.search:
        with open(logpath, "r") as file:
            txt = file.read()
        search_note(args.search, txt)

if __name__ == "__main__":
    main()
