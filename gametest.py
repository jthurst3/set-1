import unittest
from game import *
from testhelpers import *

class TestGame(unittest.TestCase):

    def setUp(self):
        self.g = Game()

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

    def testSelectState(self):
        # SELECT --> SELECT
        # TODO: should fail, add features to make it pass
        self.g.state = GameState.SELECT
        self.g.executeSelectState()
        self.assertIsInState(GameState.SELECT)

    def testUserInputState(self):
        # USER_INPUT --> USER_INPUT or NICE_SET or INVALID_SET
        # TODO: how do we test this if it involves user input?
        # until we figure out a way to do this, this test should fail
        self.assertTrue(False)

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




