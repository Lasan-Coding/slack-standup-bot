import os

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

TEST_USER_ID = os.environ["TEST_USER_ID"]

QUESTIONS = (
    "Time for standup! Three questions:\n"
    "1. Yesterday: what did you work on?\n"
    "2. Today: what are you working on?\n"
    "3. Blockers: anything in your way?"
)

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

try:
    dm = client.conversations_open(users=TEST_USER_ID)
    channel_id = dm["channel"]["id"]
    client.chat_postMessage(channel=channel_id, text=QUESTIONS)
    print("Questions sent.")
except SlackApiError as e:
    print("Slack rejected the request:", e.response["error"])
