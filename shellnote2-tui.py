#!/usr/bin/python

import curses

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

# function to print center logo
def get_logo_coords(n_row, n_col, msg):
    center_row = int(n_row/10)
    center_col = int(n_col/2)
    half_len_of_msg = int(len(msg)/2)
    x_pos = center_col - half_len_of_msg
    y_pos = center_row
    return x_pos, y_pos


# BEGIN PROGRAM
# add top line
stdscr.addstr("shellnote", curses.A_REVERSE)
stdscr.chgat(-1, curses.A_REVERSE)

# add bottom menu
stdscr.addstr(curses.LINES-1, 0, "Press 'q' to quit")

# add main window
main_window = curses.newwin(curses.LINES-2, curses.COLS, 1, 0)

# add window within the main window
text_window = main_window.subwin(curses.LINES-6, curses.COLS-4, 3, 2)
# draw border around main window
main_window.box()

# get window size
n_row, n_col = main_window.getmaxyx()

logo = ["         __         ____            __     ",
"   _____/ /_  ___  / / /___  ____  / /____ ",
"  / ___/ __ \\/ _ \\/ / / __ \\/ __ \\/ __/ _ \\",
" (__  ) / / /  __/ / / / / / /_/ / /_/  __/",
"/____/_/ /_/\\___/_/_/_/ /_/\\____/\\__/\\___/ "]

# draw logo
for i in range(len(logo)):
    x_pos, y_pos = get_logo_coords(n_row, n_col, logo[i])
    main_window.addstr(y_pos+i, x_pos, logo[i])

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
