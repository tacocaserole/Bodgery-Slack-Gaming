import os
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient


slack_events_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_SECRET']
)

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = SlackClient(
    slack_bot_token
    , endpoint="/sack/events"
)


# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event):
    emoji = event.get("reaction")
    print(emoji)


# Start the server on port
slack_events_adapter.start(
    host='10.0.1.5'
    ,port=os.environ['SLACKBOT_EVENTS_PORT']
)
