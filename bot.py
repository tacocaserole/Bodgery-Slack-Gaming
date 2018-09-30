import diceroll
import mentionrouter
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

mention_router = mentionrouter.Router()
mention_router.register( "roll",
    diceroll.DiceRollHandler( CONF["max_dice"], CONF["max_dice_size"], slack_client )
)


@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    message = event_data["event"]
    mention_router.handle_mention(
        user = message['user'],
        text = message['text'],
        channel = message['channel'],
    )


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))



# Start the server
slack_events_adapter.start(
    host=CONF["host"],
    port=CONF["port"],
    #debug=True,
)
