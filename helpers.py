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


