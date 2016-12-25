import unittest
import copy
from objects import *
from testhelpers import *

class TestHelperFunctions(unittest.TestCase):

    def testValidSet(self):
        # c1, c2, c3 is a set
        # c1, c4, c5 is a set
        c1 = Card('R','1','O','E')
        c2 = Card('R','2','O','E')
        c3 = Card('R','3','O','E')
        c4 = Card('G','2','<>','|')
        c5 = Card('P','3','S','F')
        self.assertTrue(validSet(c1, c2, c3))
        self.assertFalse(validSet(c1, c2, c4))
        self.assertTrue(validSet(c1, c4, c5))

    def testAllSame(self):
        self.assertTrue(allSame('E','E','E'))
        self.assertFalse(allSame('E','E','|'))
        self.assertFalse(allSame('E','F','|'))

    def testAllDifferent(self):
        self.assertFalse(allDifferent('E','E','E'))
        self.assertFalse(allDifferent('E','E','|'))
        self.assertTrue(allDifferent('E','F','|'))


class TestCard(unittest.TestCase):

    def setUp(self):
        self.c = Card('R','3','O','E')

    def testInit(self):
        self.assertEqual(self.c.attributes['color'], 'R')
        self.assertEqual(self.c.attributes['number'], '3')
        self.assertEqual(self.c.attributes['shape'], 'O')
        self.assertEqual(self.c.attributes['shading'], 'E')

    def testStrArray_notSelected(self):
        # length and width
        sArr = self.c.strarray(1)
        self.assertEqual(len(sArr), cardHeight)
        for s in sArr:
            self.assertEqual(len(removeCtrlSequences(s)), cardWidth)
        # borders -- make sure it's only borders
        self.assertEqual(''.join(set(sArr[0].strip())), '-')
        self.assertEqual(''.join(set(sArr[-1].strip())), '-')
        for s in sArr[1:-1]:
            self.assertEqual(removeCtrlSequences(s)[0], '|')
            self.assertEqual(removeCtrlSequences(s)[-1], '|')
        # number should be 1
        self.assertIn('1', sArr[1])
        # border should be default color if not selected
        # (i.e. have no assigned color)
        self.assertBorderHasDefaultColor(sArr)

    def testStrArray_selected(self):
        # length and width
        sArr = self.c.strarray(1, selected=True)
        self.assertEqual(len(sArr), cardHeight)
        for s in sArr:
            self.assertEqual(len(removeCtrlSequences(s)), cardWidth)
        # borders -- make sure it's only borders
        self.assertEqual(''.join(set(removeCtrlSequences(sArr[0].strip()))), '-')
        self.assertEqual(''.join(set(removeCtrlSequences(sArr[-1].strip()))), '-')
        for s in sArr[1:-1]:
            self.assertEqual(removeCtrlSequences(s)[0], '|')
            self.assertEqual(removeCtrlSequences(s)[-1], '|')
        # number should be 1
        self.assertIn('1', sArr[1])
        # border should be red by default
        self.assertBorderHasColor(sArr, bcolors.RED)

    def testStrArray_selectedGreen(self):
        # length and width
        sArr = self.c.strarray(1, selected=True, color=bcolors.GREEN)
        self.assertEqual(len(sArr), cardHeight)
        for s in sArr:
            self.assertEqual(len(removeCtrlSequences(s)), cardWidth)
        # borders -- make sure it's only borders
        self.assertEqual(''.join(set(removeCtrlSequences(sArr[0].strip()))), '-')
        self.assertEqual(''.join(set(removeCtrlSequences(sArr[-1].strip()))), '-')
        for s in sArr[1:-1]:
            self.assertEqual(removeCtrlSequences(s)[0], '|')
            self.assertEqual(removeCtrlSequences(s)[-1], '|')
        # number should be 1
        self.assertIn('1', sArr[1])
        # border should be green
        self.assertBorderHasColor(sArr, bcolors.GREEN)

    def testEq(self):
        otherCard = Card('R','3','O','E')
        self.assertEqual(self.c, otherCard)
        otherCard2 = Card('G','3','O','E')
        self.assertNotEqual(self.c, otherCard)

    # makes sure the border of a card does not have any bcolors assigned to it
    def assertBorderHasDefaultColor(self, sArr):
        # TODO: make this more modular
        colors = [bcolors.PURPLE, bcolors.GREEN, bcolors.RED, bcolors.WHITE, bcolors.END]
        # top
        for color in colors:
            self.assertNotIn(color, sArr[0])
        # bottom
        for color in colors:
            self.assertNotIn(color, sArr[-1])
        # sides
        for s in sArr[1:-1]:
            self.assertEqual(s[0], '|')
            self.assertEqual(s[-1], '|')

    def assertBorderHasColor(self, sArr, color):
        # top
        self.assertTrue(sArr[0].strip().startswith(color))
        self.assertTrue(sArr[0].strip().endswith(bcolors.END))
        # bottom
        self.assertTrue(sArr[-1].strip().startswith(color))
        self.assertTrue(sArr[-1].strip().endswith(bcolors.END))
        # sides
        for s in sArr[1:-1]:
            self.assertTrue(s.startswith(color + '|' + bcolors.END))
            self.assertTrue(s.endswith(color + '|' + bcolors.END))


class TestDeck(unittest.TestCase):

    def setUp(self):
        self.d = Deck()

    def testInit(self):
        self.assertIsNotNone(self.d.cardList)
        self.assertEqual(len(self.d.cardList), 81)
        # TODO: add more assertions for this?

    def testDealCard(self):
        card = self.d.dealCard()
        self.assertEqual(len(self.d.cardList), 80)
        self.assertIsInstance(card, Card)
        self.assertNotIn(card, self.d.cardList)

    def testIsEmpty(self):
        self.assertFalse(self.d.isEmpty())
        self.d.cardList = []
        self.assertTrue(self.d.isEmpty())

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.b = Board()

    def testInit(self):
        self.assertIsNotNone(self.b.deck)
        self.assertIsNotNone(self.b.cards)
        self.assertEqual(len(self.b.cards), 12)

    def testIsEmpty(self):
        self.assertFalse(self.b.isEmpty())
        self.b.cards = []
        self.assertTrue(self.b.isEmpty())

    def testReplaceIndex(self):
        self.b.replaceIndex(0)
        self.assertIsInstance(self.b.cards[0], Card)
        self.assertEqual(len(self.b.cards), 12)

        self.b.deck.cardList = []
        self.b.replaceIndex(0)
        self.assertIsInstance(self.b.cards[0], Card)
        self.assertEqual(len(self.b.cards), 11)

    def testAddCard(self):
        self.b.addCard()
        self.assertEqual(len(self.b.cards), 13)
        self.b.deck.cardList = []
        self.b.addCard()
        self.assertEqual(len(self.b.cards), 13)

    def testShiftCards_empty(self):
        oldCardArrangement = copy.deepcopy(self.b.cards)
        self.b.shiftCards([])
        self.assertEqual(self.b.cards, oldCardArrangement)

    def testShiftCards_inBeginning(self):
        oldCardArrangement = copy.deepcopy(self.b.cards)
        self.b.shiftCards([1, 5, 7])
        self.assertEqual(len(self.b.cards), 9)
        # cards 1, 5, 7 should be replaced by cards 11, 10, 9
        self.assertEqual(self.b.cards[1], oldCardArrangement[11])
        self.assertEqual(self.b.cards[5], oldCardArrangement[10])
        self.assertEqual(self.b.cards[7], oldCardArrangement[9])
        # other cards should have stayed the same
        for i in range(9):
            if i != 1 and i != 5 and i != 7:
                self.assertEqual(self.b.cards[i], oldCardArrangement[i])

    def testShiftCards_mixed(self):
        oldCardArrangement = copy.deepcopy(self.b.cards)
        self.b.shiftCards([1, 5, 10])
        self.assertEqual(len(self.b.cards), 9)
        # cards 1 and 5 should have been replaced by cards 11 and 9
        self.assertEqual(self.b.cards[1], oldCardArrangement[11])
        self.assertEqual(self.b.cards[5], oldCardArrangement[9])
        # other cards should have stayed the same
        for i in range(9):
            if i != 1 and i != 5:
                self.assertEqual(self.b.cards[i], oldCardArrangement[i])

    def testShiftCards_atEnd(self):
        oldCardArrangement = copy.deepcopy(self.b.cards)
        self.b.shiftCards([9, 10, 11])
        self.assertEqual(len(self.b.cards), 9)
        # no cards should be replaced
        self.assertEqual(self.b.cards, oldCardArrangement[:9])

    def testNumSets(self):
        # c1, c2, c3 is a set
        # c1, c4, c5 is a set
        c1 = Card('R','1','O','E')
        c2 = Card('R','2','O','E')
        c3 = Card('R','3','O','E')
        c4 = Card('G','2','<>','|')
        c5 = Card('P','3','S','F')
        self.b.cards = []
        self.assertEqual(self.b.numSets(), 0)
        self.assertEqual(self.b.setCountString(), '0 sets')
        self.b.cards.append(c1)
        self.assertEqual(self.b.numSets(), 0)
        self.assertEqual(self.b.setCountString(), '0 sets')
        self.b.cards.append(c2)
        self.assertEqual(self.b.numSets(), 0)
        self.assertEqual(self.b.setCountString(), '0 sets')
        self.b.cards.append(c3)
        self.assertEqual(self.b.numSets(), 1)
        self.assertEqual(self.b.setCountString(), '1 set')
        self.b.cards.append(c4)
        self.assertEqual(self.b.numSets(), 1)
        self.assertEqual(self.b.setCountString(), '1 set')
        self.b.cards.append(c5)
        self.assertEqual(self.b.numSets(), 2)
        self.assertEqual(self.b.setCountString(), '2 sets')


if __name__ == '__main__':
    helperSuite = unittest.TestLoader().loadTestsFromTestCase(TestHelperFunctions)
    unittest.TextTestRunner(verbosity=2,buffer=True).run(helperSuite)
    boardSuite = unittest.TestLoader().loadTestsFromTestCase(TestBoard)
    unittest.TextTestRunner(verbosity=2,buffer=True).run(boardSuite)

    deckSuite = unittest.TestLoader().loadTestsFromTestCase(TestDeck)
    unittest.TextTestRunner(verbosity=2,buffer=True).run(deckSuite)

    cardSuite = unittest.TestLoader().loadTestsFromTestCase(TestCard)
    unittest.TextTestRunner(verbosity=2,buffer=True).run(cardSuite)




