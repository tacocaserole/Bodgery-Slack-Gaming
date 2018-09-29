import random

class DiceRoll:
    def roll_dice( size_dice, num_dice=1 ):
        rolls = map( lambda x: random.randint( 1, size_dice ), range(num_dice) )
        return list(rolls)
