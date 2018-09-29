import os
import random
import re
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient


slack_events_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_SECRET']
    ,endpoint="/slack/events"
)
slack_client = SlackClient( os.environ["SLACK_BOT_TOKEN"] )

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

        rolls = roll_dice( size_dice, num_dice )
        sum_rolls = sum(rolls)

        roll_sep = ", "
        roll_str = roll_sep.join( list(map( lambda x: str(x), rolls )) )
        return_msg = "<@%s> rolled %s (total %s)" %(
            message["user"],
            roll_str,
            sum_rolls,
        )
        slack_client.api_call("chat.postMessage", channel=channel, text=return_msg)


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Start the server
slack_events_adapter.start(
    host='10.0.1.5',
    port=os.environ['SLACKBOT_EVENTS_PORT'],
    #debug=True,
)
