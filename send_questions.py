import os

import psycopg
from dotenv import load_dotenv
from slack_sdk import WebClient

from actions import send_questions_to_member

load_dotenv()

conn = psycopg.connect(os.environ["DATABASE_URL"])
members = conn.execute(
    "SELECT slack_user_id FROM members WHERE active = true"
).fetchall()
conn.close()

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

for (slack_user_id,) in members:
    send_questions_to_member(client, slack_user_id)
