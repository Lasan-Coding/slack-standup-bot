import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(os.environ["DATABASE_URL"])
result = conn.execute("SELECT 1").fetchone()
print("Connected. Result:", result)
conn.close()
