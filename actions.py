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
        SELECT members.name, responses.yesterday, responses.today, responses.blockers
        FROM responses
        JOIN members ON responses.member_id = members.id
        WHERE responses.standup_date = CURRENT_DATE
        """
    ).fetchall()

    if not rows:
        print("No responses today, nothing to post.")
        return False

    lines = ["*Standup digest for today*"]
    for name, yesterday, today, blockers in rows:
        lines.append(f"\n*{name}*")
        lines.append(f"Yesterday: {yesterday}")
        lines.append(f"Today: {today}")
        lines.append(f"Blockers: {blockers}")
    digest_text = "\n".join(lines)

    try:
        client.chat_postMessage(channel=channel_id, text=digest_text)
        print("Digest posted.")
        return True
    except SlackApiError as e:
        print("Slack rejected the request:", e.response["error"])
        return False
