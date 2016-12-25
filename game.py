from __future__ import print_function
from objects import *
import atexit
import signal
import subprocess
import time

# enum
# TODO: is there a better way to do enums in Python?
class GameState:
    USER_INPUT = 0
    NICE_SET = 1
    INVALID_SET = 2
    START = 6
    END = 7
    SELECT = 8


class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.state = GameState.START
        self.selectedMode = False
        # integer array representing which cards are currently selected
        self.selectedCards = []
        self.inputstatus = ''

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
        # TODO
        self.state = GameState.USER_INPUT

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
        elif cards == '?':
            self.inputstatus = 'Help not available yet :('
        elif cards == '/':
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

    def executeNiceSetState(self):
        time.sleep(1)
        c1, c2, c3 = self.selectedCards
        self.score += 1
        if len(self.board.cards) > 12:
            self.board.shiftCards([c1, c2, c3])
        else:
            self.board.replaceIndex(c1)
            self.board.replaceIndex(c2)
            self.board.replaceIndex(c3)
        self.inputstatus = ''
        self.selectedCards = []
        self.state = GameState.USER_INPUT

    def executeInvalidSetState(self):
        time.sleep(1)
        self.score -= 1
        self.inputstatus = ''
        self.selectedCards = []
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

    def display(self):
        # clear screen and put text in position
        # http://wiki.bash-hackers.org/scripting/terminalcodes#cursor_handling
        os.system("clear")
        print('\033[H')
        if self.state == GameState.NICE_SET:
            print(self.board.string(select=self.selectedCards, color=bcolors.GREEN))
        else:
            print(self.board.string(select=self.selectedCards))
        print(self.statusline())
        print('\n')

    def statusline(self):
        return self.board.setCountString() + '\t\t' + self.inputstatus + '\t\t' + self.scoreString()

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

if __name__ == '__main__':
    # save and restore screen
    # http://wiki.bash-hackers.org/scripting/terminalcodes#saverestore_screen
    saveScreen()
    atexit.register(restoreScreen)
    # restore screen on sigtstp
    #signal.signal(signal.SIGTSTP, lambda a, b: restoreScreen())
    #signal.signal(signal.SIGCONT, lambda a, b: saveScreen())
    main()
