import os

import psycopg
from dotenv import load_dotenv
from slack_sdk import WebClient

from actions import generate_and_post_digest

load_dotenv()

conn = psycopg.connect(os.environ["DATABASE_URL"])
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

generate_and_post_digest(client, conn, os.environ["SLACK_CHANNEL_ID"])

conn.close()
