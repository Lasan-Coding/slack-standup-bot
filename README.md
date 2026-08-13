# Standup Bot

An async daily standup bot for Slack. DMs each team member three questions
every weekday morning, collects responses through the day, and posts a
digest to a team channel.

## What it does

- Each weekday morning, registered team members get DMed three questions –
  yesterday, today, blockers – at 9am in their own timezone.
- Responses are collected through the day via a Slack modal, with the latest
  submission winning if someone answers twice.
- At a set time, a digest is posted to a team channel, grouped by person,
  also listing anyone who hasn't responded yet.
- No digest is posted if nobody has responded.

## Tech stack

- Python
- Postgres (via Supabase)
- `slack_bolt` / `slack_sdk` (Socket Mode – no public server required)
- `APScheduler` for timezone-aware scheduling

## Status

Built and tested against a real Slack workspace, including real per-member
timezone-aware prompts and a scheduled digest. Deployment (running
unattended, continuously) is deferred – see `DECISIONS.md`. Currently it
runs locally, when actively started.

## Running your own instance

1. Create a Slack app with these bot scopes: `chat:write`, `im:write`,
   `users:read`. Enable **Socket Mode** (generates an app-level token) and
   **Interactivity**.
2. Create a Postgres database (e.g. via [Supabase](https://supabase.com)).
3. Copy `.env.example` to `.env` and fill in your own credentials.
4. Set up a virtual environment and install dependencies:
   ```
   python -m venv venv
   ./venv/Scripts/pip install -r requirements.txt
   ```
5. Set up the schema: `./venv/Scripts/python admin/create_tables.py`
6. Register a member: `./venv/Scripts/python admin/register_member.py <slack_user_id>`
7. Run the bot: `./venv/Scripts/python bot.py`

## How this was built

Built with Claude as a technical collaborator – I directed scope and
reviewed the design decisions, not a solo unaided build. This project was
mostly about learning. See `DECISIONS.md` for the trade-offs made along
the way.

This also isn't the first tool to solve this problem – Geekbot and Slack's
own Workflow Builder both already offer versions of async standups, and are
probably better alternatives. This was built deliberately as a learning
exercise, not because nothing like it exists.

## Technical concepts

- **OAuth & scoped permissions** – Slack app authentication via bot/app-level
  tokens, incrementally requesting new scopes as functionality grew
- **Real-time event handling** – Socket Mode for receiving Slack events
  without a public-facing server
- **Relational schema design** – normalized Postgres schema (separate
  members/responses tables), foreign keys, upsert logic via `ON CONFLICT`
- **SQL injection prevention** – parameterized queries throughout
- **Timezone-aware scheduling** – IANA region names rather than fixed
  offsets, per-member local-time prompts
- **Scheduling architecture** – in-process scheduler (`APScheduler`) vs.
  OS-level cron

## Decisions log

See [DECISIONS.md](DECISIONS.md) for the running log of trade-offs made
throughout the project.
