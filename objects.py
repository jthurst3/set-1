from __future__ import print_function
import os
import random
import time

class bcolors:
   PURPLE = '\033[95m'
   GREEN = '\033[92m'
   RED = '\033[91m'
   WHITE = '\033[97m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   ITALICS = '\033[3m'
   END = '\033[0m'

# must be an even number >= 10
cardWidth = 24
# must be an odd number >= 5
cardHeight = 7
colors = {'R':bcolors.RED,'G':bcolors.GREEN,'P':bcolors.PURPLE}
shadings = {'E':bcolors.ITALICS,'F':bcolors.BOLD,'|':bcolors.UNDERLINE}
shapes = {'O':'O ','S':'S ','<>':'<>'}

def validSet(card1,card2,card3):
    for att in card1.attributes:
        att1 = card1.attributes[att]
        att2 = card2.attributes[att]
        att3 = card3.attributes[att]
        if not(allSame(att1,att2,att3) or allDifferent(att1,att2,att3)):
            return False
    return True

def allSame(att1,att2,att3):
    if att1 == att2 and att2 == att3:
        return True
    else:
        return False

def allDifferent(att1,att2,att3):
    if not att1 == att2 and not att2 == att3 and not att1 == att3:
        return True
    else:
        return False


class Card():
    def __init__(self,color,number,shape,shading):
        self.attributes = {'color':color,'number':number,'shape':shape,'shading':shading}
    #def __str__(self):
    #    return ' '.join([self.attributes['color'],self.attributes['number'],self.attributes['shape'],self.attributes['shading']])
    def __hash__(self):
        colors = ['R','G','P']
        shadings = ['E','F','|']
        shapes = ['O','S','<>']
        numbers = ['1','2','3']
        return (27*colors.index(self.attributes['color']) +
                9*shadings.index(self.attributes['shading']) +
                3*shapes.index(self.attributes['shape']) +
                numbers.index(self.attributes['number']))

    def __str__(self):
        st = colors[self.attributes['color']]
        st += shadings[self.attributes['shading']]
        for i in range(int(self.attributes['number'])):
            st += shapes[self.attributes['shape']]
        st += bcolors.END
        return st

    def strarray(self, cardnum, selected=False, color=bcolors.RED):
        """string array representing how the card looks when printed (with borders).
        Because we'll need to piece together each row of each card when we're printing
        the board, the string at index i of this array represents how row i should look.
        If selected is True, border and card number will be red.
        """
        numTopInnerRows = (cardHeight - 4)/2
        numBottomInnerRows = numTopInnerRows + 1
        assert numTopInnerRows + numBottomInnerRows + 4 == cardHeight
        colorPrefix = ''
        colorPostfix = ''
        if selected:
            colorPrefix = color
            colorPostfix = bcolors.END
        # top and bottom border
        tB = colorPrefix + ''.join(['-' for _ in range(cardWidth-2)]) + colorPostfix
        # vertical border 
        vB = colorPrefix + '|' + colorPostfix
        cardNumber = colorPrefix + str(cardnum) + colorPostfix
        rows = []
        # first row is all dashes
        rows.append(' ' + tB + ' ')
        # second row contains card number
        rows.append(vB +
                cardNumber +
                ''.join([' ' for _ in range(cardWidth-2-len(str(cardnum)))]) +
                vB)
        # bunch of middle rows contain blanks
        for _ in range(numTopInnerRows):
            rows.append(vB + ''.join([' ' for _ in range(cardWidth-2)]) + vB)
        # middle row contains contents of the card
        numLeftSpaces = (cardWidth-2-2*int(self.attributes['number']))/2
        numRightSpaces = numLeftSpaces
        assert numLeftSpaces + numRightSpaces + 2 + 2*int(self.attributes['number']) == cardWidth
        rows.append(vB + 
                ''.join([' ' for _ in range(numLeftSpaces)]) +
                str(self) +
                ''.join([' ' for _ in range(numRightSpaces)]) +
                vB)
        # bunch of middle rows contain blanks
        for _ in range(numBottomInnerRows):
            rows.append(vB + ''.join([' ' for _ in range(cardWidth-2)]) + vB)
        # last row is all dashes
        rows.append(' ' + tB + ' ')
        return rows

    def __eq__(self, otherCard):
        return isinstance(otherCard, Card) and self.attributes == otherCard.attributes

class Deck():
    def __init__(self):
        self.cardList = self.initialize_cards()
    def isEmpty(self):
        return len(self.cardList) == 0
    def initialize_cards(self):
        cards = []
        colors = ['R','G','P']
        numbers = ['1','2','3'] #consider changing from strings to ints
        shapes = ['O','S','<>']
        shadings = ['E','F','|']
        for color in colors:
            for number in numbers:
                for shape in shapes:
                    for shading in shadings:
                        cards.append(Card(color,number,shape,shading))
        return cards

    def dealCard(self):
        #if the deck is empty, return error
        if self.isEmpty():
            return 'NoCards'
        #remove and return a random card from the deck
        cardIndex = random.randint(0,len(self.cardList)-1)
        card = self.cardList[cardIndex]
        del self.cardList[cardIndex]
        return card

class Board():
    def __init__(self):
        self.deck = Deck()
        self.cards = self.initialize_cards()
        self.statusline = ''
        # keep a cache of the last time we computed the number of sets
        self._cards = []
        self._numSets = 0
    def initialize_cards(self):
        cards = []
        for i in range(12):
            cards.append(self.deck.dealCard())
        return cards
    def isEmpty(self):
        return len(self.cards) == 0
    #def display(self):
        #for i in range(len(self.cards)):
            #if i%3 == 0:
                #print('\n\n')
            #print('\t\t' + str(self.cards[i]),end = '')
    def string(self, select=[], color=bcolors.RED):
        s = ''
        numRows = len(self.cards)/3
        for row in range(numRows):
            rowStrings = []
            for i in range(3*row,3*(row+1)):
                isSelected = (i in select)
                rowStrings.append(self.cards[i].strarray(i, selected=isSelected, color=color))
            # wtf this is so cool
            # http://stackoverflow.com/questions/6473679/transpose-list-of-lists
            transpose = map(list, zip(*rowStrings))
            # add the 3 cards in the row to the string
            s += '\n'.join([''.join([s for s in cardRow]) for cardRow in transpose])
            s += '\n'
        return s
    def __str__(self):
        return self.string()
    def display(self, select=[], color=bcolors.RED):
        """Displays the cards on the board, with red or green borders around the selected cards.
        """
        print(self.string(select=select, color=color))
        print(self.statusline)
    def replaceIndex(self,i):
        nextCard = self.deck.dealCard()
        if nextCard == 'NoCards':
            del self.cards[i]
        else:
            self.cards[i] = nextCard
    def addCard(self):
        nextCard = self.deck.dealCard()
        if nextCard != 'NoCards':
            self.cards.append(nextCard)
    def shiftCards(self,cs):
        numLeftoverCards = len(self.cards) - len(cs)
        replacers = [x for x in cs if x < numLeftoverCards]
        overs = [i for i in range(numLeftoverCards, len(self.cards)) if i not in
                cs]
        for r in replacers:
            index = overs.pop()
            self.cards[r] = self.cards[index]
        self.cards = self.cards[:numLeftoverCards]

    def numSets(self):
        # retrieve value from cache if available
        if set(self.cards) == set(self._cards):
            return self._numSets
        setCount = 0
        for i in range(len(self.cards)):
            for j in range(i):
                for k in range(j):
                    c1 = self.cards[i]
                    c2 = self.cards[j]
                    c3 = self.cards[k]
                    if validSet(c1, c2, c3):
                        setCount += 1
        return setCount

    def setCountString(self):
        setCountStr = ''
        setCount = self.numSets()
        setCountStr += str(setCount) + ' set'
        if setCount != 1:
            setCountStr += 's'
        return setCountStr

    def printSetCount(self):
        print(self.setCountString())


