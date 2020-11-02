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
