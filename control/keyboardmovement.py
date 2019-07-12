import curses
import os
import power
import processkey

# intializes curses globally.

stdscr = curses.initscr()

# start motion. Note - make sure visudo config file is updated for user to skip password authentication)
os.system("sudo service motion start")

def keyboard():
    # power saving - turn off idle services
    result = power.powercheck()
    if result is True:
        power.poweroff()
        time.sleep(3)     # give time for voltage to normalize

    sec = .1 #time per

    # set up curses
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    while 1:
        c = stdscr.getch()
        result = chr(c)
        processresult = processkey.processkey(result)
        if processresult is False:
            endkeyboard()
            break

def endkeyboard():
    #reset settings
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    #cleanup curses
    curses.endwin()
    #exit motion (webcam)
    os.system("sudo service motion stop")

if __name__ == "__main__":
    keyboard()
    # endkeyboard()