from mock import MagicMock
import unittest
import game
from game import *
import helpers
from helpers import *
import time

# TODO:
#   - test other states going to select state
#   - test new game functionality (including staying in select state)
#   - refactor tests to take duplicate testing code and put it into functions

class TestGame(unittest.TestCase):

    def setUp(self):
        self.g = Game()
        time.sleep = MagicMock()

    def testInit(self):
        self.assertIsNotNone(self.g.board)
        self.assertEquals(self.g.score, 0)
        self.assertIsInState(GameState.START)
        self.assertEquals(len(self.g.selectedCards), 0)

    def assertIsInState(self, state):
        return self.assertEquals(self.g.state, state)

    def testValidateInput_specialInput(self):
        self.assertEqual(self.g.validateInput('add'), 'add')
        self.assertEqual(self.g.validateInput('?'), '?')
        self.assertEqual(self.g.validateInput('/'), '/')

    def testValidateInput_invalidInput(self):
        self.assertIsNone(self.g.validateInput(None))
        self.assertIsNone(self.g.validateInput(''))
        self.assertIsNone(self.g.validateInput('0 1'))
        self.assertIsNone(self.g.validateInput('0 1 2 3'))
        self.assertIsNone(self.g.validateInput('a b c'))
        self.assertIsNone(self.g.validateInput('2 -1 3'))
        self.assertIsNone(self.g.validateInput('3 14 2'))
        self.assertIsNone(self.g.validateInput('2 3 3'))
        self.assertIsNone(self.g.validateInput('2 2 3'))
        # limit is currently 11
        self.assertIsNone(self.g.validateInput('2 3 12'))

    def testValidateInput_validInput(self):
        self.assertEqual(self.g.validateInput('0 3 11'), [0, 3, 11])
        self.assertEqual(self.g.validateInput('11 0 3'), [0, 3, 11])
        # append some dummy cards
        self.g.board.cards.extend(['hello','lia','klein'])
        self.assertEqual(self.g.validateInput('2 3 12'), [2, 3, 12])

    def testStartState(self):
        # START --> USER_INPUT
        self.g.state = GameState.START
        self.g.executeStartState()
        self.assertIsInState(GameState.USER_INPUT)

    def testSelectState_invalidInput(self):
        # SELECT --> SELECT
        self.g.state = GameState.SELECT
        helpers.getch = MagicMock(return_value='~')
        self.g.setSelectedMode()
        self.g.executeSelectState()
        self.assertEqual(self.g.inputstatus, 'Invalid character with ASCII value ' + str(ord('~')))
        self.assertTrue(game.selectedMode)
        self.assertEqual(len(self.g.selectedCards), 0)
        self.assertEqual(len(self.g.board.cards), 12)
        self.assertEqual(self.g.labels, selectKeys)
        self.assertIsInState(GameState.SELECT)

    def testSelectState_toggleCard(self):
        # SELECT --> SELECT
        self.g.state = GameState.SELECT
        self.g.setSelectedMode()
        # toggle
        helpers.getch = MagicMock(return_value='1')
        self.g.executeSelectState()
        self.assertEqual(self.g.inputstatus, '')
        self.assertTrue(game.selectedMode)
        self.assertEqual(len(self.g.selectedCards), 1)
        self.assertEqual(self.g.selectedCards, [0])
        self.assertIsInState(GameState.SELECT)
        # un-toggle
        helpers.getch = MagicMock(return_value='1')
        self.g.executeSelectState()
        self.assertEqual(self.g.inputstatus, '')
        self.assertEqual(len(self.g.selectedCards), 0)
        self.assertIsInState(GameState.SELECT)

    def testSelectState_toggleSelectState(self):
        # SELECT --> USER_INPUT
        self.g.state = GameState.SELECT
        self.g.setSelectedMode()
        # toggle
        helpers.getch = MagicMock(return_value='/')
        self.g.executeSelectState()
        self.assertEqual(self.g.inputstatus, '')
        self.assertFalse(game.selectedMode)
        self.assertEqual(len(self.g.selectedCards), 0)
        self.assertIsInState(GameState.USER_INPUT)
        self.assertEqual(self.g.labels,
                ['0','1','2','3','4','5','6','7','8','9','10','11'])

    def testSelectState_help(self):
        # SELECT --> SELECT
        self.g.state = GameState.SELECT
        self.g.setSelectedMode()
        helpers.getch = MagicMock(return_value='?')
        self.g.executeSelectState()
        # TODO: not implemented
        self.assertTrue(False)

    def testUserInputState_invalidInput(self):
        # USER_INPUT --> USER_INPUT
        self.g.state = GameState.USER_INPUT
        self.g.getUserInput = MagicMock(return_value='asdf')
        self.g.executeUserInputState()
        self.assertEqual(self.g.inputstatus, 'Invalid input')
        self.assertFalse(game.selectedMode)
        self.assertEqual(len(self.g.selectedCards), 0)
        self.assertEqual(len(self.g.board.cards), 12)
        self.assertEqual(self.g.labels,
                ['0','1','2','3','4','5','6','7','8','9','10','11'])
        self.assertIsInState(GameState.USER_INPUT)

    def testUserInputState_add(self):
        # USER_INPUT --> USER_INPUT
        self.g.state = GameState.USER_INPUT
        self.g.getUserInput = MagicMock(return_value='add')
        self.g.executeUserInputState()
        self.assertEqual(self.g.inputstatus, '')
        self.assertFalse(game.selectedMode)
        self.assertEqual(len(self.g.selectedCards), 0)
        self.assertEqual(len(self.g.board.cards), 15)
        self.assertEqual(self.g.labels,
                ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
        self.assertIsInState(GameState.USER_INPUT)

    def testUserInputState_help(self):
        # USER_INPUT --> USER_INPUT
        self.g.state = GameState.USER_INPUT
        self.g.getUserInput = MagicMock(return_value='?')
        self.g.executeUserInputState()
        # TODO: not implemented (should fail)
        self.assertTrue(False)
        self.assertFalse(game.selectedMode)
        self.assertEqual(len(self.g.selectedCards), 0)
        self.assertEqual(len(self.g.board.cards), 12)
        self.assertEqual(self.g.labels,
                ['0','1','2','3','4','5','6','7','8','9','10','11'])
        self.assertIsInState(GameState.USER_INPUT)

    def testUserInputState_select(self):
        # USER_INPUT --> SELECT
        self.g.state = GameState.USER_INPUT
        self.g.getUserInput = MagicMock(return_value='/')
        self.g.executeUserInputState()
        self.assertEqual(self.g.inputstatus, '')
        self.assertTrue(game.selectedMode)
        self.assertEqual(len(self.g.selectedCards), 0)
        self.assertEqual(len(self.g.board.cards), 12)
        self.assertEqual(self.g.labels, selectKeys)
        self.assertIsInState(GameState.SELECT)

    def testUserInputState_niceSet(self):
        # c1, c2, c3 is a set
        c1 = Card('R','1','O','E')
        c2 = Card('R','2','O','E')
        c3 = Card('R','3','O','E')
        # USER_INPUT --> NICE_SET
        self.g.state = GameState.USER_INPUT
        self.g.board.cards[:3] = [c1, c2, c3]
        self.g.getUserInput = MagicMock(return_value='0 1 2')
        self.g.executeUserInputState()
        self.assertEqual(self.g.inputstatus, 'Nice set')
        self.assertFalse(game.selectedMode)
        self.assertEqual(len(self.g.selectedCards), 3)
        self.assertEqual(len(self.g.board.cards), 12)
        self.assertEqual(self.g.labels,
                ['0','1','2','3','4','5','6','7','8','9','10','11'])
        self.assertIsInState(GameState.NICE_SET)

    def testUserInputState_invalidSet(self):
        # c1, c2, c3 is not a set
        c1 = Card('R','1','O','E')
        c2 = Card('R','2','O','E')
        c3 = Card('G','3','O','E')
        # USER_INPUT --> INVALID_SET
        self.g.state = GameState.USER_INPUT
        self.g.board.cards[:3] = [c1, c2, c3]
        self.g.getUserInput = MagicMock(return_value='0 1 2')
        self.g.executeUserInputState()
        self.assertEqual(self.g.inputstatus, 'Invalid set')
        self.assertFalse(game.selectedMode)
        self.assertEqual(len(self.g.selectedCards), 3)
        self.assertEqual(len(self.g.board.cards), 12)
        self.assertEqual(self.g.labels,
                ['0','1','2','3','4','5','6','7','8','9','10','11'])
        self.assertIsInState(GameState.INVALID_SET)

    # TODO: mock out the time.sleep call
    def testNiceSetState_12Cards(self):
        self.g.state = GameState.NICE_SET
        # pretending that the first 3 cards are a set
        self.g.selectedCards = [0, 1, 2]
        self.g.executeNiceSetState()
        self.assertEquals(len(self.g.selectedCards), 0)
        self.assertEquals(len(self.g.board.cards), 12)
        self.assertIsInState(GameState.USER_INPUT)
        self.assertEquals(self.g.score, 1)

    # TODO: mock out the time.sleep call
    def testNiceSetState_15Cards(self):
        self.g.state = GameState.NICE_SET
        self.g.board.addCard()
        self.g.board.addCard()
        self.g.board.addCard()
        # pretending that the first 3 cards are a set
        self.g.selectedCards = [0, 1, 2]
        self.g.executeNiceSetState()
        self.assertEquals(len(self.g.selectedCards), 0)
        self.assertEquals(len(self.g.board.cards), 12)
        self.assertIsInState(GameState.USER_INPUT)
        self.assertEquals(self.g.score, 1)

    # TODO: mock out the time.sleep call
    def testInvalidSetState(self):
        self.g.state = GameState.INVALID_SET
        # pretending that the first 3 cards are not a set
        self.g.selectedCards = [0, 1, 2]
        self.g.executeInvalidSetState()
        self.assertEquals(self.g.score, -1)
        self.assertEquals(len(self.g.selectedCards), 0)
        self.assertEquals(len(self.g.board.cards), 12)
        self.assertIsInState(GameState.USER_INPUT)

    def testStatusLine(self):
        self.g.inputstatus = 'set is cool'
        s = self.g.statusline()
        self.assertIn(self.g.board.setCountString(), s)
        self.assertIn(self.g.inputstatus, s)
        self.assertIn(self.g.scoreString(), s)

    def testScoreString(self):
        # negative score should be red
        self.g.score = -1
        s = self.g.scoreString()
        self.assertEquals(removeCtrlSequences(s), 'Score: -1')
        self.assertTrue(s.startswith(bcolors.RED))
        self.assertTrue(s.endswith(bcolors.END))
        # neutral score should be default color
        self.g.score = 0
        s = self.g.scoreString()
        self.assertEquals(removeCtrlSequences(s), 'Score: 0')
        self.assertEquals(s, removeCtrlSequences(s))
        # positive score should be green
        self.g.score = 1
        s = self.g.scoreString()
        self.assertEquals(removeCtrlSequences(s), 'Score: 1')
        self.assertTrue(s.startswith(bcolors.GREEN))
        self.assertTrue(s.endswith(bcolors.END))



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGame)
    unittest.TextTestRunner(verbosity=2,buffer=True).run(suite)




