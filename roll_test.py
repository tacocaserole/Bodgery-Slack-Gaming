import unittest
import diceroll

class TestRoll(unittest.TestCase):
    '''roll dice'''
    def test_roll(self):
        roll = diceroll.DiceRoll.roll_dice( 6 )
        self.assertEqual( len(roll), 1, "Correct number of rolls" )
        self.assertLessEqual( roll[0], 6, "Correct top size" )
        self.assertGreaterEqual( roll[0], 1, "Correct bottom size" );

    def test_many_rolls(self):
        roll = diceroll.DiceRoll.roll_dice( 10, 5 )
        self.assertEqual( len(roll), 5, "Correct number of rolls" )
