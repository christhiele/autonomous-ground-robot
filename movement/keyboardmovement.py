from drivepwm import *
import curses

stdscr = curses.initscr()

def keyboard():
    sec = .1
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    while 1:
        c = stdscr.getch()
        if c == ord('w'):
            forward(sec)
        elif c == ord('s'):
            reverse(sec)
        elif c == ord('a'):
            partialleft(sec, 0)
        elif c == ord('d'):
            partialright(sec, 0)
        elif c == ord('q'):
            partialleft(sec, 50)
        elif c == ord('e'):
            partialright(sec, 50)
        elif c == ord('z'):
            pivotleft(sec)
        elif c == ord('c'):
            pivotright(sec)
        elif c == ord('x'):
            stop(sec)
        elif c == ord('r'):
            break
    endkeyboard()

def endkeyboard():
    #reset pwm
    cleanuppwm()
    #reset settings
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    #cleanup
    curses.endwin()

if __name__ == "__main__":
    keyboard()