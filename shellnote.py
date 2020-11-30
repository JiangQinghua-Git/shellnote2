#!/usr/bin/env python3

import argparse
import os
import sys
from time import strftime
from re import search
import curses
from signal import signal, SIGINT, SIGTERM

homedir = os.path.expanduser("~")
configfile = "config.py"
configpath = os.path.join(homedir, ".config", "shellnote", configfile)
version_str = "0.2.0"

if os.path.exists(configpath):
    exec(open(configpath).read())
else:
    logdir = homedir
    logfile = "shellnote.txt"
    logpath = os.path.join(logdir, logfile)
    delim = "\t"

def add_note(text, quiet=False):
    entry_date = strftime("%Y-%m-%d")
    entry_time = strftime("%H:%M")
    entry = entry_date + delim + entry_time + delim + text
    with open(logpath, "a") as file:
        file.write(entry + "\n")
    if not quiet:
        print(f"Added entry to {logpath}")

def print_notes(logpath):
    with open(logpath, "r") as f:
        for i in f:
            print(i, end='')

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
            print_notes(logpath)
    
        if args.edit:
            launch_editor()
        
        if args.input:
            text = input("Note: ")
            entry = add_note(text, args.quiet)
    
        if args.search:
            with open(logpath, "r") as f:
                txt = f.read()
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
        self.stdscr.keypad(True)
        
        # check for color support, if so start colors
        if curses.has_colors():
            curses.start_color()
        
        # create colors 
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
        
        # get terminal size
        self.Y, self.X = self.stdscr.getmaxyx()
        
        # define menu items
        # the key in the dict is the text of the menu item that appears
        # the value is the character to be underlined
        self.menu_items = {
                "Add note":1, 
                "Browse notes":1,
                "Edit notes":1, 
                "Change config":1,
                "Help":1, 
                "Quit":1}
        self.menu_funcs = [
                self.add_note_tui, 
                self.browse_notes,
                self.launch_editor_tui, 
                self.change_config,
                self.draw_help_window, 
                self.shutdown] 

        # BEGIN PROGRAM
        self.event_loop()


    def launch_editor_tui(self):
        # TODO: fix bug where, after having exited the editor (vim) and returned to
        # shellnote, screen is not cleared after issuing quit command 
        launch_editor()
        self.stdscr.clear()
        #self.stdscr.refresh()
        #self.shutdown()

    def add_note_tui(self):
        # TODO: popup a small window which takes user input and sends to add_note
        self.draw_dummy_window()

    def browse_notes(self):
        # TODO: draw scrollable window with print of all notes 
        # add top or bottom menu that can apply filters (date, tag)
        self.draw_dummy_window()
        #pad = curses.newpad(2000,self.X-4)
        #for y in range(0,1000):
        #    for x in range(0,self.X-5):
        #        pad.addstr(y, x, '10')
        #pad.refresh(0,0, 1,2, self.Y-3,self.X-4)
        #self.stdscr.getch()

    def change_config(self):
        # TODO: make function look for config file, copy default one to user
        # dir if it doesn't exist, then open it in editor
        self.draw_dummy_window()

    def draw_all(self):
        self.draw_main_window()
        self.draw_menu_window(self.y_logo)
        self.draw_menu_items()

    # event loop
    def event_loop(self):
        self.menu_choice = 1
        while True:
            self.draw_all()

            c = self.menu_window.getch() # wait for input
            
            # menu navigation
            if c == ord('j') or c == ord('J'):
                if self.menu_choice < len(self.menu_items):
                    self.menu_choice += 1
            elif c == ord('k') or c == ord('K'):
                if self.menu_choice > 1:
                    self.menu_choice -= 1
            elif c == ord('l') or c == curses.KEY_ENTER or c == 10 or c == 13:
                # KEY_ENTER may not work, so check for ascii newline (\n; 10) 
                # and carriage return (\r; 13)
                self.launch_menu_choice(self.menu_choice)

            # menu keyboard shortcuts
            elif c == ord('a') or c == ord('A'):
                self.add_note_tui()
            elif c == ord('e') or c == ord('E'):
                self.launch_editor_tui()
            elif c == ord('b') or c == ord('B'):
                self.browse_notes()
            elif c == ord('c') or c == ord('C'):
                self.change_config()
            elif c == ord('h') or c == ord('H'): 
                self.draw_help_window()
            elif c == ord('q') or c == ord('Q'):
                self.shutdown()

            # refresh windows from bottom up (avoids flickering)
            self.stdscr.noutrefresh()
            curses.doupdate()

        self.shutdown()

    def launch_menu_choice(self, choice):
        self.menu_funcs[choice-1]()

    def draw_help_window(self):
        height = 12
        width = int(0.6*self.X)
        y, x = self.get_window_center(self.Y, self.X, width)
        self.help_window = curses.newwin(height, width,
                self.y_logo-2, x) 
        help_text = "This is a helpful text." 
        self.help_window.addstr(1, 3, help_text) 
        self.help_window.box()
        self.help_window.noutrefresh()
        curses.doupdate()
        self.help_window.getch() # wait for any key press
        self.stdscr.clear()
    
    def draw_dummy_window(self):
        height = 12
        width = int(0.6*self.X)
        y, x = self.get_window_center(self.Y, self.X, width)
        self.help_window = curses.newwin(height, width,
                self.y_logo-2, x) 
        help_text = "Coming soon..." 
        self.help_window.addstr(1, 3, help_text) 
        self.help_window.box()
        self.help_window.noutrefresh()
        curses.doupdate()
        self.help_window.getch() # wait for any key press
        self.stdscr.clear()
    
    def draw_menu_window(self, y_start):
        line_pad = 3 # lines to pad after logo
        y_menu = y_start + line_pad # y coord where menu begins
        menu_height = len(self.menu_items) + 2 
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
        menu_pad = 2 # padding columns 
        for i, (key, value) in enumerate(self.menu_items.items(), 1):
            if i == self.menu_choice:
                # highlight menu choice and underline keybind
                self.menu_window.addstr(i, menu_pad, "%s" % key, curses.A_STANDOUT)
                self.menu_window.chgat(i, value+1, 1, curses.A_UNDERLINE | curses.A_STANDOUT)
            else:
                self.menu_window.addstr(i, menu_pad, "%s" % key)
                self.menu_window.chgat(i, value+1, 1, curses.A_UNDERLINE)
        # update windows
        self.menu_window.noutrefresh()
        # redraw the screen
        curses.doupdate()
    
    def draw_main_window(self):
        # add top line
        #self.stdscr.addstr("shellnote", curses.A_REVERSE)
        #self.stdscr.chgat(-1, curses.A_REVERSE)
        
        # add bottom menu
        self.stdscr.addstr(curses.LINES-1, 0, "Press 'q' to quit.")
        
        # add main window
        self.main_window = curses.newwin(self.Y-1, self.X, 0, 0)
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

    # function to get center of window wrt a length d
    def get_window_center(self, y, x, d):
        y_center = int(y/2)
        x_center = int(x/2)
        half_len_of_d = int(d/2)
        x = x_center - half_len_of_d
        return y, x

    def kill_curses(self):
        # restore terminal settings and quit
        curses.nocbreak()
        curses.echo()
        self.stdscr.keypad(False)
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
