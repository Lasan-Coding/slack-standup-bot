import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

with open("admin/schema.sql") as f:
    schema = f.read()

conn = psycopg.connect(os.environ["DATABASE_URL"])
conn.execute(schema)
conn.commit()
conn.close()
print("Tables created.")
