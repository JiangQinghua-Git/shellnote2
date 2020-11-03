#!/usr/bin/python

import argparse
import os
import sys
from time import strftime
from re import search
import yaml
import curses

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

def add_note(text, quiet=False):
    entry_date = strftime("%Y-%m-%d")
    entry_time = strftime("%H:%M:%S")
    entry_id = hash(entry_date+entry_time) 
    entry_tags = None
    entry = [{"id": entry_id, "date": entry_date, "time": entry_time, 
         "tags": entry_tags, "note": text}]
    entry = yaml.dump(entry, sort_keys=False) # make yaml format
    with open(logpath, "a") as file:
        file.write(entry + "\n")
    if not quiet:
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

class CLI:
    def __init__(self):
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
                action="store_true")
        
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
            text = input("Note: ")
            entry = add_note(text, args.quiet)
    
        if args.search:
            with open(logpath, "r") as file:
                txt = file.read()
            search_note(args.search, txt)
        # if no arguments provided, launch curses tui
        if not any(vars(args).values()):
            tui = TUI()
        #    exec(open("shellnote-tui.py").read())

class TUI:
    def __init__(self):
        # initialize standard screen
        stdscr = curses.initscr()
        # disable echo, character break and cursor
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        
        # check for color support, if so start colors
        if curses.has_colors():
            curses.start_color()
        
        # create colors 
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
        
        # function to get center of window wrt a length d
        def get_window_center(y, x, d):
            y_center = int(y/2)
            x_center = int(x/2)
            half_len_of_d = int(d/2)
            x = x_center - half_len_of_d
            return y, x
        
        # BEGIN PROGRAM
        # add top line
        stdscr.addstr("shellnote", curses.A_REVERSE)
        stdscr.chgat(-1, curses.A_REVERSE)
        
        # add bottom menu
        stdscr.addstr(curses.LINES-1, 0, "Press 'q' to quit.")
        
        # get terminal size
        Y, X = stdscr.getmaxyx()
        
        # add main window
        #main_window = curses.newwin(curses.LINES-2, curses.COLS, 1, 0)
        main_window = curses.newwin(Y-2, X, 1, 0)
        # draw border around main window
        main_window.box()
        # get window size
        n_row, n_col = main_window.getmaxyx()
        
        logo = [
        "         __         ____            __     ",
        "   _____/ /_  ___  / / /___  ____  / /____ ",
        "  / ___/ __ \\/ _ \\/ / / __ \\/ __ \\/ __/ _ \\",
        " (__  ) / / /  __/ / / / / / /_/ / /_/  __/",
        "/____/_/ /_/\\___/_/_/_/ /_/\\____/\\__/\\___/ ",
        "$ Easy note-taking on the command line.  "]
        
        # draw logo
        for i in range(len(logo)):
            y, x = get_window_center(Y, X, len(logo[i]))
            main_window.addstr(1+i, x, logo[i])
        
        y_menu = i + 4 # y coord where menu begins
        h_menu = 6 
        w_menu = 20
        # add menu window within the main window
        y, x = get_window_center(Y, X, w_menu)
        menu_window = main_window.subwin(
                h_menu, w_menu, 
                y_menu, x)
        menu_window.box()
        menu_window.addstr(1, 2, ">")
        menu_window.addstr(1, 4, "Add note")
        menu_window.addstr(1+1, 4, "Edit notes")
        menu_window.addstr(1+2, 4, "Browse notes")
        menu_window.addstr(1+3, 4, "Help")
        
        # update windows
        stdscr.noutrefresh()
        main_window.noutrefresh()
        
        # redraw the screen
        curses.doupdate()
        
        # event loop
        while True:
            c = main_window.getch()
        
            if c == ord('q') or c == ord('Q'):
                break
        
            # refresh windows from bottom up (avoids flickering)
            stdscr.noutrefresh()
            main_window.noutrefresh()
            text_window.noutrefresh()
            curses.doupdate()
        
        # restore terminal settings
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        
        # end program
        curses.endwin()

def main():
    cli = CLI()

if __name__ == "__main__":
    main()
