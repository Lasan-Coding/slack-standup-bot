import os

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
channel = os.environ["SLACK_CHANNEL_ID"]

try:
    client.chat_postMessage(channel=channel, text="Standup bot is alive.")
    print("Message sent.")
except SlackApiError as e:
    print("Slack rejected the message:", e.response["error"])
