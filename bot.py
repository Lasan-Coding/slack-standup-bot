import os

import psycopg
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])


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
    ack()
    values = view["state"]["values"]
    yesterday = values["yesterday_block"]["yesterday_input"]["value"]
    today = values["today_block"]["today_input"]["value"]
    blockers = values["blockers_block"]["blockers_input"]["value"]
    slack_user_id = body["user"]["id"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    member_id = conn.execute(
        "SELECT id FROM members WHERE slack_user_id = %s", (slack_user_id,)
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
        (member_id, yesterday, today, blockers),
    )
    conn.commit()
    conn.close()
    print("Response stored for", slack_user_id)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("Bot is listening. Ctrl+C to stop.")
    handler.start()
