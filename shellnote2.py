#!/usr/bin/python

from argparse import ArgumentParser
import os
from time import strftime
import re

LOG_DIR = os.getenv("HOME") 
LOG_FILE = "shellnote2.txt"
LOG_PATH = LOG_DIR + "/" + LOG_FILE
delim = "\t"
version_str = "0.1"

def add_note(note):
     date = strftime("%Y-%m-%d")
     time = strftime("%H:%M")
     entry = date+delim+time+delim+note
     with open(LOG_PATH, "a") as file:
         file.write(entry + "\n")

def search_note(search_term, txt):
    txt_split = txt.splitlines()
    indexes = []
    for i in range(len(txt_split)):
        match = re.search(search_term, txt_split[i])
        if match:
            indexes.append(i)
    result = [txt_split[i] for i in indexes]
    for i in range(len(result)):
        print(result[i])

def main():
    ap = ArgumentParser(description="shellnote2: easy note-taking on the command line.")
    
    ## arguments
    ap.add_argument("-a", "--add", help="add note", action="store")
    ap.add_argument("-e", "--edit", help="edit current entries in your text editor", action="store_true")
    ap.add_argument("-i", "--input", help="add note by input prompt", action="store_true")
    ap.add_argument("-p", "--print", help="print entries", action="store_true")
    ap.add_argument("-s", "--search", help="search entries", action="store")
    ap.add_argument("-v", "--version", action="version", version=version_str)
    ap.add_argument("-q", "--quiet", help="suppress output", action="store_true")
    
    args = ap.parse_args()

    if args.add:
        add_note(args.add)
        if not args.quiet:
            print(f"Added entry to {LOG_PATH}")
    
    if args.edit:
        if "EDITOR" in os.environ:
            os.system(f"$EDITOR {LOG_PATH}")
        else:
            os.system(f"vim {LOG_PATH}")
    
    if args.input:
        note = input("Note: ")
        add_note(note)
        if not args.quiet:
            print(f"Added entry to {LOG_PATH}")

    if args.print:
        with open(LOG_PATH, "r") as file:
            print(file.read())
    
    if args.search:
        with open(LOG_PATH, "r") as file:
            txt = file.read()
        search_note(args.search, txt)

if __name__ == "__main__":
    main()
