# Standup Bot

Async daily standup bot for Slack. Portfolio project — see also
`DECISIONS.md` for the running log of technical trade-offs.

## What it does

Each weekday morning it DMs every registered team member three questions. It
collects responses through the day. At a set time it posts one digest to a team
channel summarising who said what, and who didn't respond.

That is the entire product.

## Scope

**In scope**
- Scheduled DM prompts to registered members, in each member's own timezone
- Three questions: yesterday / today / blockers
- Response collection and storage, keyed to person and standup date
- Latest response wins if someone answers twice
- Scheduled digest posted to one channel, grouped by person, listing non-responders
- No digest posted if nobody responded
- Admin via CLI script or slash command — no UI needed

**Out of scope** — push back if I ask for these
- Web dashboard, analytics, trend charts
- AI summarisation of responses
- Multi-workspace support
- Mobile anything

## Stack

- Python
- Postgres (chosen over SQLite deliberately, as a learning goal — see DECISIONS.md)
- Deployed to a free-tier host
- Secrets via environment variables

## Build order

Check in with me between each step.

1. Slack app registered, credentials working, bot posts one message to one channel
2. Database connected; review schema with me before creating tables
3. Send the three questions to one hardcoded user
4. Store a response
5. Generate and post a digest for that one user
6. Multiple users, read from the database
7. Scheduling and timezones
8. Failure handling and edge cases
9. Deploy
10. README, including the decisions log

## Definition of done

Runs unattended for a full week on a real Slack workspace with at least two
people in it, and I can explain any part of the codebase without looking it up.

## Working notes

My general working preferences live in `~/.claude/CLAUDE.md` and apply here.
Project-specific additions:

- Update `DECISIONS.md` whenever a real trade-off is made. Prompt me if I forget.
- Deliberate failure testing is part of the project, not a distraction. When I
  break something on purpose, help me read the error rather than just fixing it.
