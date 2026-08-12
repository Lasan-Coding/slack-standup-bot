import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

TEST_USER_ID = os.environ["TEST_USER_ID"]

conn = psycopg.connect(os.environ["DATABASE_URL"])

conn.execute(
    """
    INSERT INTO members (slack_user_id, name, timezone)
    VALUES (%s, %s, %s)
    ON CONFLICT (slack_user_id) DO NOTHING
    """,
    (TEST_USER_ID, "Lasan", "Europe/Berlin"),
)

member_id = conn.execute(
    "SELECT id FROM members WHERE slack_user_id = %s", (TEST_USER_ID,)
).fetchone()[0]

conn.execute(
    """
    INSERT INTO responses (member_id, standup_date, yesterday, today, blockers)
    VALUES (%s, CURRENT_DATE, %s, %s, %s)
    ON CONFLICT (member_id, standup_date)
    DO UPDATE SET
        yesterday = EXCLUDED.yesterday,
        today = EXCLUDED.today,
        blockers = EXCLUDED.blockers,
        submitted_at = now()
    """,
    (member_id, "test: fixed a bug", "test: writing more code", "test: none"),
)

conn.commit()
conn.close()
print("Response stored.")
