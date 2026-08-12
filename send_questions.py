import os

import psycopg
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

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

conn = psycopg.connect(os.environ["DATABASE_URL"])
members = conn.execute(
    "SELECT slack_user_id FROM members WHERE active = true"
).fetchall()
conn.close()

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

for (slack_user_id,) in members:
    try:
        dm = client.conversations_open(users=slack_user_id)
        channel_id = dm["channel"]["id"]
        client.chat_postMessage(
            channel=channel_id, blocks=BLOCKS, text="Time for standup!"
        )
        print("Message sent to", slack_user_id)
    except SlackApiError as e:
        print("Slack rejected the request for", slack_user_id, ":", e.response["error"])
