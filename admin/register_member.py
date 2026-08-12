import os
import sys

import psycopg
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

if len(sys.argv) != 2:
    print("Usage: python register_member.py <slack_user_id>")
    sys.exit(1)

slack_user_id = sys.argv[1]

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

try:
    result = client.users_info(user=slack_user_id)
except SlackApiError as e:
    print("Slack rejected the request:", e.response["error"])
    sys.exit(1)

user = result["user"]
name = user["real_name"]
timezone = user["tz"]

conn = psycopg.connect(os.environ["DATABASE_URL"])
conn.execute(
    """
    INSERT INTO members (slack_user_id, name, timezone)
    VALUES (%s, %s, %s)
    ON CONFLICT (slack_user_id)
    DO UPDATE SET name = EXCLUDED.name, timezone = EXCLUDED.timezone
    """,
    (slack_user_id, name, timezone),
)
conn.commit()
conn.close()

print(f"Registered {name} ({slack_user_id}), timezone {timezone}")
