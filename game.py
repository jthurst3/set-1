from __future__ import print_function
from objects import *
from helpers import *
import atexit
import signal
import subprocess
import sys
import termios
import time
import tty

# enum
# TODO: is there a better way to do enums in Python?
class GameState:
    USER_INPUT = 0
    NICE_SET = 1
    INVALID_SET = 2
    START = 6
    END = 7
    SELECT = 8

# TODO: what about for boards with more than 12 cards?
selectKeys = ['1','2','3','q','w','e','a','s','d','z','x','c']

class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.state = GameState.START
        self.selectedMode = False
        # integer array representing which cards are currently selected
        self.selectedCards = []
        self.inputstatus = ''
        self.labels = [str(i) for i in range(len(self.board.cards))]
        self._labelStart = 0
        # TODO: this is not accurate, but accurate enough for our calculations
        self.screenWidth = cardWidth*3

    def getUserInput(self):
        return raw_input("\n\nPlease Enter Set in space separated list (e.g. 0 10 4): ")

    def validateInput(self, userInput):
        if not userInput:
            return
        cards = userInput.strip()
        if cards == 'add' or cards == '?' or cards == '/':
            return cards
        cards = cards.split(' ')
        if len(cards) != 3:
            return
        # try to convert input to integers
        intCards = []
        for card in cards:
            try:
                intCard = int(card)
                intCards.append(intCard)
            except ValueError:
                return
        # numbers should be between 0 (inclusive) and numCards (exclusive) no duplicates
        numCards = len(self.board.cards)
        intCards.sort()
        if intCards[0] < 0 or intCards[2] >= numCards or intCards[0] == intCards[1] or intCards[1] == intCards[2]:
            return
        return intCards

    def executeStartState(self):
        self.state = GameState.USER_INPUT

    def executeSelectState(self):
        # parse one character at a time
        ch = getch()
        # user pressed a key corresponding to a card
        if ch in selectKeys:
            self.inputstatus = ''
            ind = selectKeys.index(ch) + self._labelStart
            if ind in self.selectedCards:
                self.selectedCards.remove(ind)
            else:
                self.selectedCards.append(ind)
        # toggle select mode
        elif ch == '/':
            self.inputstatus = ''
            self.unsetSelectedMode()
            self.state = GameState.USER_INPUT
        # up
        elif ord(ch) == 65:
            self.shiftLabelsUp()
        # down
        elif ord(ch) == 66:
            self.shiftLabelsDown()
        # Ctrl+C
        elif ord(ch) == 3 or ord(ch) == 4:
            system.exit(1)
        # add sets
        elif ch == '+':
            # TODO: replicated code with what's in self.executeUserInputState()
            self.inputstatus = ''
            self.board.addCard()
            self.board.addCard()
            self.board.addCard()
            self.selectedCards = []
            self.labels = ['' for i in range(len(self.board.cards))]
            self.labels[self._labelStart:self._labelStart+len(selectKeys)] = selectKeys
        # process a set
        elif ch == '\n' or ch == '\r':
            # process the set
            if len(self.selectedCards) != 3:
                self.inputstatus = 'Invalid input'
                self.selectedCards = []
            else:
                c1, c2, c3 = self.selectedCards
                if validSet(self.board.cards[c1], self.board.cards[c2], self.board.cards[c3]):
                    self.inputstatus = bcolors.GREEN+'Nice set'+bcolors.END
                    self.state = GameState.NICE_SET
                else:
                    self.inputstatus = bcolors.RED+'Invalid set'+bcolors.END
                    self.state = GameState.INVALID_SET
        # unknown, show ASCII character number for debugging
        else:
            self.inputstatus = 'Invalid character with ASCII value ' + str(ord(ch))

    def executeUserInputState(self):
        inp = self.getUserInput()
        cards = self.validateInput(inp)
        if not cards:
            self.inputstatus = 'Invalid input'
        elif cards == 'add':
            self.inputstatus = ''
            self.board.addCard()
            self.board.addCard()
            self.board.addCard()
            self.labels = [str(i) for i in range(len(self.board.cards))]
        elif cards == '?':
            self.inputstatus = 'Help not available yet :('
        elif cards == '/':
            self.setSelectedMode()
            self.state = GameState.SELECT
        else:
            c1, c2, c3 = cards
            self.selectedCards = cards
            if validSet(self.board.cards[c1], self.board.cards[c2], self.board.cards[c3]):
                self.inputstatus = 'Nice set'
                self.state = GameState.NICE_SET
            else:
                self.inputstatus = 'Invalid set'
                self.state = GameState.INVALID_SET

    # NOTE: need to manually change state
    def setSelectedMode(self):
        self.selectedMode = True
        self.labels = ['' for i in range(len(self.board.cards))]
        self.labels[:len(selectKeys)] = selectKeys
        self.selectedCards = []
        self._labelStart = 0

    # NOTE: need to manually change state
    def unsetSelectedMode(self):
        self.selectedMode = False
        self.labels = [str(i) for i in range(len(self.board.cards))]
        self.selectedCards = []

    # visually up
    def shiftLabelsUp(self):
        if self._labelStart == 0:
            return
        self._labelStart -= 3
        self.labels = ['' for i in range(len(self.board.cards))]
        self.labels[self._labelStart:self._labelStart+len(selectKeys)] = selectKeys

    # visually down
    def shiftLabelsDown(self):
        if self._labelStart + len(selectKeys) >= len(self.board.cards):
            return
        self._labelStart += 3
        self.labels = ['' for i in range(len(self.board.cards))]
        self.labels[self._labelStart:self._labelStart+len(selectKeys)] = selectKeys

    def executeNiceSetState(self):
        time.sleep(1)
        c1, c2, c3 = self.selectedCards
        self.score += 1
        if len(self.board.cards) > 12:
            self.board.shiftCards([c1, c2, c3])
            if self._labelStart + len(selectKeys) > len(self.board.cards):
                self.shiftLabelsUp()
        else:
            self.board.replaceIndex(c1)
            self.board.replaceIndex(c2)
            self.board.replaceIndex(c3)
        self.inputstatus = ''
        self.selectedCards = []
        if self.board.deck.isEmpty() and self.board.numSets() == 0:
            self.state = GameState.END
        elif self.selectedMode:
            self.state = GameState.SELECT
        else:
            self.state = GameState.USER_INPUT

    def executeInvalidSetState(self):
        time.sleep(1)
        self.score -= 1
        self.inputstatus = ''
        self.selectedCards = []
        if self.selectedMode:
            self.state = GameState.SELECT
        else:
            self.state = GameState.USER_INPUT

    def play(self):
        while self.state != GameState.END:
            self.display()
            # should have a switch statement... does Python have one?
            if self.state == GameState.START:
                self.executeStartState()
            elif self.state == GameState.SELECT:
                self.executeSelectState()
            elif self.state == GameState.USER_INPUT:
                self.executeUserInputState()
            elif self.state == GameState.NICE_SET:
                self.executeNiceSetState()
            elif self.state == GameState.INVALID_SET:
                self.executeInvalidSetState()
            else:
                print('Invalid game state ', self.state, 'exiting.')
                sys.exit(1)
        time.sleep(2)

    def display(self):
        # clear screen and put text in position
        # http://wiki.bash-hackers.org/scripting/terminalcodes#cursor_handling
        os.system("clear")
        print('\033[H')
        color = bcolors.RED
        if self.state == GameState.NICE_SET:
            color = bcolors.GREEN
        elif self.state == GameState.SELECT:
            color = bcolors.PURPLE
        print(self.board.string(self.labels, select=self.selectedCards, color=color))
        print(self.statusline())
        print('\n')

    # make the status line the width of the screen
    def statusline(self):
        # set count on left
        setCountString = self.board.setCountString()
        # input status in center
        inputStatus = self.inputstatus
        # score on right
        scoreString = self.scoreString()
        setCountStart = 0
        inputStatusStart = (self.screenWidth - len(removeCtrlSequences(inputStatus)))/2
        scoreStringStart = self.screenWidth - len(removeCtrlSequences(scoreString)) + (
                len(inputStatus) - len(removeCtrlSequences(inputStatus)))
        # make string array
        s = [' ' for _ in range(self.screenWidth)]
        s[setCountStart:setCountStart+len(setCountString)] = setCountString
        s[inputStatusStart:inputStatusStart+len(inputStatus)] = inputStatus
        s[scoreStringStart:scoreStringStart+len(scoreString)] = scoreString
        return ''.join(s)

    def scoreString(self):
        scoreStr = 'Score: ' + str(self.score)
        if self.score > 0:
            return bcolors.GREEN + scoreStr + bcolors.END
        elif self.score < 0:
            return bcolors.RED + scoreStr + bcolors.END
        else:
            return scoreStr

def main():
    game = Game()
    game.play()

def saveScreen():
    subprocess.call(['tput','smcup'])

def restoreScreen():
    subprocess.call(['tput','rmcup'])

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

if __name__ == '__main__':
    # save and restore screen
    # http://wiki.bash-hackers.org/scripting/terminalcodes#saverestore_screen
    saveScreen()
    atexit.register(restoreScreen)
    # restore screen on sigtstp
    #signal.signal(signal.SIGTSTP, lambda a, b: restoreScreen())
    #signal.signal(signal.SIGCONT, lambda a, b: saveScreen())
    main()
