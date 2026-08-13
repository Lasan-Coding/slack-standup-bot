from datetime import datetime, time
from zoneinfo import ZoneInfo

from slack_sdk.errors import SlackApiError

STANDUP_BLOCKS = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Time for standup! Click below to answer today's questions.",
        },
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "Fill in standup"},
                "action_id": "open_standup_modal",
            }
        ],
    },
]

PROMPT_HOUR = time(9, 0)


def send_questions_to_member(client, slack_user_id):
    try:
        dm = client.conversations_open(users=slack_user_id)
        channel_id = dm["channel"]["id"]
        client.chat_postMessage(
            channel=channel_id, blocks=STANDUP_BLOCKS, text="Time for standup!"
        )
        print("Message sent to", slack_user_id)
        return True
    except SlackApiError as e:
        print(
            "Slack rejected the request for", slack_user_id, ":", e.response["error"]
        )
        return False


def generate_and_post_digest(client, conn, channel_id):
    rows = conn.execute(
        """
        SELECT members.name, members.timezone, responses.submitted_at,
               responses.yesterday, responses.today, responses.blockers
        FROM members
        LEFT JOIN responses
            ON responses.member_id = members.id
            AND responses.standup_date = CURRENT_DATE
        WHERE members.active = true
        """
    ).fetchall()

    responded = []
    non_responders = []
    for name, member_timezone, submitted_at, yesterday, today, blockers in rows:
        if submitted_at is not None:
            responded.append((name, yesterday, today, blockers))
        else:
            now_local = datetime.now(ZoneInfo(member_timezone))
            if now_local.time() >= PROMPT_HOUR:
                non_responders.append(name)

    if not responded:
        print("No responses today, nothing to post.")
        return False

    lines = ["*Standup digest for today*"]
    for name, yesterday, today, blockers in responded:
        lines.append(f"\n*{name}*")
        lines.append(f"Yesterday: {yesterday}")
        lines.append(f"Today: {today}")
        lines.append(f"Blockers: {blockers}")

    if non_responders:
        lines.append(f"\n*Didn't respond:* {', '.join(non_responders)}")

    digest_text = "\n".join(lines)

    try:
        client.chat_postMessage(channel=channel_id, text=digest_text)
        print("Digest posted.")
        return True
    except SlackApiError as e:
        print("Slack rejected the request:", e.response["error"])
        return False
