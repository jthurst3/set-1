import sys
import termios
import tty
from objects import *

# removes terminal control sequences defined in bcolors from a string
# TODO: make this more modular
def removeCtrlSequences(s):
    cSequences = [bcolors.PURPLE, bcolors.GREEN, bcolors.RED, bcolors.WHITE, bcolors.BOLD,
            bcolors.UNDERLINE, bcolors.ITALICS, bcolors.END]
    newS = s
    for c in cSequences:
        newS = newS.replace(c, '')
    return newS

# gets one character from stdin, without waiting for a newline
# TODO: really hacky
# http://code.activestate.com/recipes/134892/
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

