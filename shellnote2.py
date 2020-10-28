#!/bin/python

import argparse
import os

LOG_DIR = os.getenv("HOME") 
LOG_FILE = "shellnote2.txt"
LOG_PATH = LOG_DIR + "/" + LOG_FILE

def main():
    parser = argparse.ArgumentParser(description="shellnote2: easy note-taking on the command line.")
    
    ## arguments
    parser.add_argument("-q", "--quiet", help="suppress output", action="store_true")
    parser.add_argument("-a", "--add", help="add note")
    
    args = parser.parse_args()

    if args.add:
        note = args.add
        with open(LOG_PATH, "a") as file:
            file.write(note + "\n")
        if not args.quiet:
            print(f"Entry added: {note}")

if __name__ == "__main__":
    main()
