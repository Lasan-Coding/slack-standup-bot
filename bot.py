import os
from datetime import datetime, time
from zoneinfo import ZoneInfo

import psycopg
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from actions import PROMPT_HOUR, generate_and_post_digest, send_questions_to_member

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

DIGEST_TIMEZONE = "Europe/Berlin"


def check_and_send_questions():
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    members = conn.execute(
        "SELECT slack_user_id, timezone, last_prompted_date"
        " FROM members WHERE active = true"
    ).fetchall()

    for slack_user_id, member_timezone, last_prompted_date in members:
        now_local = datetime.now(ZoneInfo(member_timezone))
        is_due = now_local.time() >= PROMPT_HOUR
        already_sent = last_prompted_date == now_local.date()

        if is_due and not already_sent:
            success = send_questions_to_member(app.client, slack_user_id)
            if success:
                conn.execute(
                    "UPDATE members SET last_prompted_date = %s"
                    " WHERE slack_user_id = %s",
                    (now_local.date(), slack_user_id),
                )
                conn.commit()

    conn.close()


def check_and_post_digest():
    now_berlin = datetime.now(ZoneInfo(DIGEST_TIMEZONE))
    if now_berlin.time() < time(10, 30):
        return

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    already_posted = conn.execute(
        "SELECT 1 FROM digest_log WHERE posted_date = %s", (now_berlin.date(),)
    ).fetchone()

    if not already_posted:
        success = generate_and_post_digest(
            app.client, conn, os.environ["SLACK_CHANNEL_ID"]
        )
        if success:
            conn.execute(
                "INSERT INTO digest_log (posted_date) VALUES (%s)",
                (now_berlin.date(),),
            )
            conn.commit()

    conn.close()


def run_scheduled_checks():
    check_and_send_questions()
    check_and_post_digest()


@app.action("open_standup_modal")
def open_modal(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "standup_submission",
            "title": {"type": "plain_text", "text": "Daily Standup"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "yesterday_block",
                    "label": {"type": "plain_text", "text": "Yesterday"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "yesterday_input",
                    },
                },
                {
                    "type": "input",
                    "block_id": "today_block",
                    "label": {"type": "plain_text", "text": "Today"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "today_input",
                    },
                },
                {
                    "type": "input",
                    "block_id": "blockers_block",
                    "label": {"type": "plain_text", "text": "Blockers"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "blockers_input",
                    },
                },
            ],
        },
    )


@app.view("standup_submission")
def handle_submission(ack, body, view):
    values = view["state"]["values"]
    yesterday = values["yesterday_block"]["yesterday_input"]["value"]
    today = values["today_block"]["today_input"]["value"]
    blockers = values["blockers_block"]["blockers_input"]["value"]
    slack_user_id = body["user"]["id"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    row = conn.execute(
        "SELECT id FROM members WHERE slack_user_id = %s", (slack_user_id,)
    ).fetchone()

    if row is None:
        conn.close()
        print("Submission from unregistered member:", slack_user_id)
        ack()
        return

    member_id = row[0]
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
        (member_id, yesterday, today, blockers),
    )
    conn.commit()
    conn.close()
    ack()
    print("Response stored for", slack_user_id)


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scheduled_checks, "interval", minutes=5, next_run_time=datetime.now())
    scheduler.start()

    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("Bot is listening (v2). Ctrl+C to stop.")
    handler.start()
