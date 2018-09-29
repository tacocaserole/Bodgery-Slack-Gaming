import diceroll
import yaml
import random
import re
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient


def get_config( conf_file ):
    with open( conf_file ) as x: conf_str = x.read()
    conf = yaml.load( conf_str )
    return conf


CONF = get_config( "config.yaml" )
slack_events_adapter = SlackEventAdapter(
    CONF["slack_signing_secret"],
    endpoint="/slack/events"
)
slack_client = SlackClient( CONF["slack_bot_token"] )

roll_match = re.compile( "roll (\d+)?d(\d+)" )

random.seed()


def roll_dice( size_dice, num_dice=1 ):
    rolls = map( lambda x: random.randint( 1, size_dice ), range(num_dice) )
    return list(rolls)

@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    message = event_data["event"]
    channel = message["channel"]

    match = roll_match.search( message.get( 'text' ) )
    if match is not None:
        num_dice = match.group(1)
        num_dice = 1 if num_dice is None else int( num_dice )
        size_dice = int( match.group(2) )

        return_msg = ""
        try:
            dice = diceroll.DiceRoll(
                max_dice=CONF['max_dice'],
                max_size=CONF['max_dice_size'],
            )
            rolls = dice.roll( size_dice, num_dice )
            sum_rolls = sum( rolls )

            roll_sep = ", "
            roll_str = roll_sep.join( list(map( lambda x: str(x), rolls )) )
            return_msg = "<@%s> rolled %s (total %s)" %(
                message["user"],
                roll_str,
                sum_rolls,
            )
        except diceroll.DiceTooBigException as e:
            return_msg = "<@%s> Sorry, I can only handle up to %s sized dice" %( message["user"], e.max_allowed_size )
        except diceroll.TooManyDiceException as e:
            return_msg = "<@%s> Sorry, I can only handle up to %s dice at once" %( message["user"], e.max_allowed_dice )
            
        slack_client.api_call("chat.postMessage", channel=channel, text=return_msg)


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))



# Start the server
slack_events_adapter.start(
    host=CONF["host"],
    port=CONF["port"],
    #debug=True,
)
