#!/usr/bin/python

import argparse
import os
from time import strftime

LOG_DIR = os.getenv("HOME") 
LOG_FILE = "shellnote2.txt"
LOG_PATH = LOG_DIR + "/" + LOG_FILE
delim = "\t"

def add_note(note):
     date = strftime("%Y-%m-%d")
     time = strftime("%H:%M")
     entry = date+delim+time+delim+note
     with open(LOG_PATH, "a") as file:
         file.write(entry + "\n")

def main():
    parser = argparse.ArgumentParser(description="shellnote2: easy note-taking on the command line.")
    
    ## arguments
    parser.add_argument("-q", "--quiet", help="suppress output", action="store_true")
    parser.add_argument("-a", "--add", help="add note")
    parser.add_argument("-p", "--print", help="print entries", action="store_true")
    parser.add_argument("-e", "--edit", help="edit current entries in your text editor", action="store_true")
    parser.add_argument("-i", "--input", help="add note by input prompt", action="store_true")

    args = parser.parse_args()

    if args.add:
        add_note(args.add)
        if not args.quiet:
            print(f"Added entry to {LOG_PATH}")
    
    if args.print:
        with open(LOG_PATH, "r") as file:
            print(file.read())
    
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

if __name__ == "__main__":
    main()
