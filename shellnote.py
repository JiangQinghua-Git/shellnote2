#!/usr/bin/python

import argparse
import os
import sys
from time import strftime
from re import search
import yaml
import curses
from signal import signal, SIGINT, SIGTERM

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


class TUI:
    
    def __init__(self):

        # tell curses to shutdown gracefully at terminal kill signal
        signal(SIGINT, self.shutdown)
        signal(SIGTERM, self.shutdown)

        # initialize standard screen
        self.stdscr = curses.initscr()
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
        
        # get terminal size
        self.Y, self.X = self.stdscr.getmaxyx()
        
        # BEGIN PROGRAM
        self.draw_main_window()
        # draw menu starting at bottom y pos of logo
        self.draw_menu_window(self.y_logo)
        #self.draw_menu_items()
        self.event_loop()


    def draw_main_window(self):
        # add top line
        self.stdscr.addstr("shellnote", curses.A_REVERSE)
        self.stdscr.chgat(-1, curses.A_REVERSE)
        
        # add bottom menu
        self.stdscr.addstr(curses.LINES-1, 0, "Press 'q' to quit.")
        
        # add main window
        self.main_window = curses.newwin(self.Y-2, self.X, 1, 0)
        # draw border around main window
        self.main_window.box()
        
        # draw logo
        self.y_logo = self.draw_logo()

        # update windows
        self.stdscr.noutrefresh()
        self.main_window.noutrefresh()

        # redraw the screen
        curses.doupdate()
    
    def draw_logo(self):    
        logo = [
        "         __         ____            __     ",
        "   _____/ /_  ___  / / /___  ____  / /____ ",
        "  / ___/ __ \\/ _ \\/ / / __ \\/ __ \\/ __/ _ \\",
        " (__  ) / / /  __/ / / / / / /_/ / /_/  __/",
        "/____/_/ /_/\\___/_/_/_/ /_/\\____/\\__/\\___/ ",
        "$ Easy note-taking on the command line.  "]
        
        # draw logo
        for i in range(len(logo)):
            y, x = self.get_window_center(self.Y, self.X, len(logo[i]))
            self.main_window.addstr(1+i, x, logo[i])
        return i # return bottom y pos

    # event loop
    def event_loop(self):
        self.menu_choice = 1
        while True:
            self.draw_menu_items()
            
            c = self.menu_window.getch() # wait for input
        
            if c == ord('q') or c == ord('Q'):
                self.shutdown()
            elif c == ord('j') or c == ord('J'):
                self.menu_choice += 1
            elif c == ord('h') or c == ord('H'): 
                self.stdscr.addstr("HELP ME! ")
        
            # refresh windows from bottom up (avoids flickering)
            self.stdscr.noutrefresh()
            curses.doupdate()
        self.shutdown()
        
    # function to get center of window wrt a length d
    def get_window_center(self, y, x, d):
        y_center = int(y/2)
        x_center = int(x/2)
        half_len_of_d = int(d/2)
        x = x_center - half_len_of_d
        return y, x

    def draw_menu_window(self, y_start):
        y_menu = y_start + 4 # y coord where menu begins
        menu_height = 6 
        menu_width = 20
        # add menu window within the main window
        y, x = self.get_window_center(self.Y, self.X, menu_width)
        self.menu_window = curses.newwin(
                menu_height, menu_width, 
                y_menu, x)
        self.menu_window.box()
        # update windows
        self.menu_window.noutrefresh()
        # redraw the screen
        curses.doupdate()

    def draw_menu_items(self):
        self.menu_items = ["Add note", "Edit notes", "Browse notes", "Help"]
        menu_pad = 2 
        for i, item in enumerate(self.menu_items, 1):
            if i == self.menu_choice:
                self.menu_window.addstr(i, menu_pad, "> %s" % item)
            else:
                self.menu_window.addstr(i, menu_pad, "  %s" % item)
        # update windows
        self.menu_window.noutrefresh()
        # redraw the screen
        curses.doupdate()
    
    def kill_curses(self):
        # restore terminal settings and quit
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()

    def shutdown(self, arg1=None, arg2=None):
        # signal() sends two args, so we need two dummy args
        self.kill_curses()
        sys.exit(0)


    
def main():
    cli = CLI()

if __name__ == "__main__":
    main()