import os

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

TEST_USER_ID = os.environ["TEST_USER_ID"]

BLOCKS = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Time for standup! Click below to answer today's questions.",
        },
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "Fill in standup"},
                "action_id": "open_standup_modal",
            }
        ],
    },
]

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

try:
    dm = client.conversations_open(users=TEST_USER_ID)
    channel_id = dm["channel"]["id"]
    client.chat_postMessage(
        channel=channel_id, blocks=BLOCKS, text="Time for standup!"
    )
    print("Message sent.")
except SlackApiError as e:
    print("Slack rejected the request:", e.response["error"])
