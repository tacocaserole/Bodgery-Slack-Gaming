import os
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient


slack_events_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_SECRET']
    ,endpoint="/slack/events"
)
slack_client = SlackClient( os.environ["SLACK_BOT_TOKEN"] )


@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    message = event_data["event"]
    channel = message["channel"]
    message = "Hello <@%s>! :tada:" % message["user"]
    slack_client.api_call("chat.postMessage", channel=channel, text=message)


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Start the server
slack_events_adapter.start(
    host='10.0.1.5'
    ,port=os.environ['SLACKBOT_EVENTS_PORT']
    #,debug=True
)
