import os

import psycopg
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

conn = psycopg.connect(os.environ["DATABASE_URL"])
rows = conn.execute(
    """
    SELECT members.name, responses.yesterday, responses.today, responses.blockers
    FROM responses
    JOIN members ON responses.member_id = members.id
    WHERE responses.standup_date = CURRENT_DATE
    """
).fetchall()
conn.close()

if not rows:
    print("No responses today, nothing to post.")
else:
    lines = ["*Standup digest for today*"]
    for name, yesterday, today, blockers in rows:
        lines.append(f"\n*{name}*")
        lines.append(f"Yesterday: {yesterday}")
        lines.append(f"Today: {today}")
        lines.append(f"Blockers: {blockers}")
    digest_text = "\n".join(lines)

    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    try:
        client.chat_postMessage(
            channel=os.environ["SLACK_CHANNEL_ID"], text=digest_text
        )
        print("Digest posted.")
    except SlackApiError as e:
        print("Slack rejected the request:", e.response["error"])
