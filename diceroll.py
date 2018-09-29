import random

class DiceTooBigException(Exception):
    def __init__( self, asked_size, max_allowed_size ):
        self.asked_size = asked_size
        self.max_allowed_size = max_allowed_size

class TooManyDiceException(Exception):
    def __init__( self, asked_dice, max_allowed_dice ):
        self.asked_dice = asked_dice
        self.max_allowed_dice = max_allowed_dice

class DiceRoll:
    def __init__( self, max_dice=128, max_size=1024 ):
        self.max_dice = max_dice
        self.max_size = max_size

    def roll( self, size_dice, num_dice=1 ):
        if size_dice > self.max_size:
            raise DiceTooBigException( size_dice, self.max_size )
        if num_dice > self.max_dice:
            raise TooManyDiceException( num_dice, self.max_dice )

        rolls = map( lambda x: random.randint( 1, size_dice ), range(num_dice) )
        return list(rolls)
