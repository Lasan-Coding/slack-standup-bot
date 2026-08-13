import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(os.environ["DATABASE_URL"])
conn.execute("ALTER TABLE members ADD COLUMN last_prompted_date DATE")
conn.execute(
    """
    CREATE TABLE digest_log (
        posted_date DATE PRIMARY KEY
    )
    """
)
conn.commit()
conn.close()
print("Added last_prompted_date column and digest_log table.")
