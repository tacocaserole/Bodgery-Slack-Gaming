import random
import mentionrouter
import re

random.seed()
roll_match = re.compile( "(\d+)?d(\d+)" )


class DiceTooBigException(Exception):
    """Thrown when the size of the die is too big"""
    def __init__( self, asked_size, max_allowed_size ):
        self.asked_size = asked_size
        self.max_allowed_size = max_allowed_size

class TooManyDiceException(Exception):
    """Thrown when the number of dice is too big"""
    def __init__( self, asked_dice, max_allowed_dice ):
        self.asked_dice = asked_dice
        self.max_allowed_dice = max_allowed_dice

class DiceRoll:
    def __init__( self, max_dice=128, max_size=1024 ):
        self.max_dice = max_dice
        self.max_size = max_size

    def roll( self, size_dice, num_dice=1 ):
        """Rolls dice of the given size and number. Returns a list of the rolls."""
        if size_dice > self.max_size:
            raise DiceTooBigException( size_dice, self.max_size )
        if num_dice > self.max_dice:
            raise TooManyDiceException( num_dice, self.max_dice )

        rolls = map( lambda x: random.randint( 1, size_dice ), range(num_dice) )
        return list(rolls)

class DiceRollHandler( mentionrouter.Handler ):
    """A mentionrouter.Handler that parses the message and rolls dice accordingly"""
    def __init__( self, max_dice, max_dice_size, slack_client ):
        self.max_dice = max_dice
        self.max_dice_size = max_dice_size
        self.slack_client = slack_client

    def handle_mention( self, from_user, to_user, cmd, remaining_msg, channel ):
        match = roll_match.search( remaining_msg )

        return_msg = ""
        if match is not None:
            num_dice = match.group(1)
            num_dice = 1 if num_dice is None else int( num_dice )
            size_dice = int( match.group(2) )

            try:
                dice = DiceRoll(
                    max_dice = self.max_dice,
                    max_size = self.max_dice_size,
                )
                rolls = dice.roll( size_dice, num_dice )
                sum_rolls = sum( rolls )

                roll_sep = ", "
                roll_str = roll_sep.join( list(map( lambda x: str(x), rolls )) )
                return_msg = "<@%s> rolled %s (total %s)" %(
                    from_user,
                    roll_str,
                    sum_rolls,
                )
            except DiceTooBigException as e:
                return_msg = "<@%s> Sorry, I can only handle up to %s sized dice" %( from_user, e.max_allowed_size )
            except TooManyDiceException as e:
                return_msg = "<@%s> Sorry, I can only handle up to %s dice at once" %( from_user, e.max_allowed_dice )
                
        else:
            return_msg = "<@%s> Sorry, I don't know how to roll that. Try something like 'roll 2d10'" %( from_user )
            
        self.slack_client.api_call( "chat.postMessage",
            channel = channel,
            text = return_msg,
        )
