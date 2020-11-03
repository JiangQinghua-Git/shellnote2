#!/usr/bin/python

import curses
import pdb

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

# function to get center of window wrt string length 
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
stdscr.addstr(curses.LINES-1, 0, "Press 'q' to quit")

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
menu_window.addstr(1+3, 4, "About")

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
