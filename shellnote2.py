#!/bin/python

import argparse
import os
from time import strftime

LOG_DIR = os.getenv("HOME") 
LOG_FILE = "shellnote2.txt"
LOG_PATH = LOG_DIR + "/" + LOG_FILE
delim = "\t"

def main():
    parser = argparse.ArgumentParser(description="shellnote2: easy note-taking on the command line.")
    
    ## arguments
    parser.add_argument("-q", "--quiet", help="suppress output", action="store_true")
    parser.add_argument("-a", "--add", help="add note")
    
    args = parser.parse_args()

    if args.add:
        date = strftime("%Y-%m-%d")
        time = strftime("%H:%M")
        entry = date+delim+time+delim+args.add
        with open(LOG_PATH, "a") as file:
            file.write(entry + "\n")
        if not args.quiet:
            print(f"Entry added: {entry}")

if __name__ == "__main__":
    main()
