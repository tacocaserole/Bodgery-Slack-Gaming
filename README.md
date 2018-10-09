# Bodgery-Slack-Gaming
A Slackbot for managing D&D character sheets, and allowing die rolls.

## Setup

1. Run "pip3 install -r requirements.txt" to install prereqs
2. Copy config.yaml.example to config.yaml
2. Go to https://api.slack.com/apps?new_app=1 to create a new app
3. Add a 'Bots' feature type
4. Put in the name and display name
5. Go to "Basic Information" in the sidebar
6. Do "Install your app to your workspace"
7. Go to "OAuth Tokens"
8. Set the Bot User OAuth Token in the "slack_bot_token" key in the config
7. Go back to "Basic Information" and find the "App Credentials" section
9. Set the Signing Secret in the "slack_signing_secret" key in the config
10. Set your assigned port number in the "port" key in the config
11. Start your server with:
    python3 bot.py
12. Back in the Slack App Manager, go to the "Basic Information" page
13. Click "Add features and functionality", and add "Event Subscriptions"
14. Turn it on, and set the URL to:
    https://XXXX.shop.thebodgery.org/slack/events
    Replacing 'XXXX' with your assigned URL prefix
15. Under "Subscribe to Bot Events", set "app_mention"
16. Hit "Save Changes"
