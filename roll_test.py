import unittest
import diceroll

class TestRoll(unittest.TestCase):
    '''roll dice'''
    def test_roll(self):
        roll = diceroll.DiceRoll().roll( 6 )
        self.assertEqual( len(roll), 1, "Correct number of rolls" )
        self.assertLessEqual( roll[0], 6, "Correct top size" )
        self.assertGreaterEqual( roll[0], 1, "Correct bottom size" );

    def test_many_rolls(self):
        roll = diceroll.DiceRoll().roll( 10, 5 )
        self.assertEqual( len(roll), 5, "Correct number of rolls" )

    def test_limits(self):
        dice = diceroll.DiceRoll( max_dice=5, max_size=20 )
        dice.roll( 20, 5 )
        self.assertTrue( True, "Can roll dice at limit" )
        
        self.assertRaises( diceroll.DiceTooBigException, dice.roll, 21, 5 )
        self.assertRaises( diceroll.TooManyDiceException, dice.roll, 20, 6 )
