#!/bin/python

import argparse

def main():
    parser = argparse.ArgumentParser()
    
    ## arguments
    parser.add_argument("-v", "--verbose", help="turn on output verbosity", action="store_true")
    parser.add_argument("-a", "--add", help="add note")
    
    args = parser.parse_args()

    #if args.verbose:
    #    print("Verbosity turned on.")

    if args.add:
        note = args.add
        if args.verbose:
            print(f"Entry added: {note}")
    #with open("shellnote.txt", "a") as file:
    #    file.write(note+"\n")

if __name__ == "__main__":
    main()
