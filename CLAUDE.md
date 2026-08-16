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
- Docker (containerized; verified on Railway, not kept running continuously — see DECISIONS.md)
- GitHub Actions for CI — builds the Docker image and publishes it to
  GitHub Container Registry on push to main
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
   - 9a. ~~Oracle Cloud Always Free VM~~ — abandoned, see DECISIONS.md
   - 9b. App containerized with Docker; runs correctly via `docker run` locally
   - 9c. GitHub Actions workflow builds the Docker image and publishes it
     to GitHub Container Registry on push to `main`
   - 9d. Verified working on Railway (a real cloud host) — prompted,
     collected a response, posted a digest correctly; torn down
     afterward rather than kept running continuously, see DECISIONS.md
10. README, including the decisions log

## Definition of done

Runs correctly against a real Slack workspace when actively running —
locally, via `docker run`, or on a cloud host (verified on Railway).
Continuous, unattended hosting is a deliberate choice not to maintain
right now, not an unverified capability — see `DECISIONS.md`.

## Working notes

My general working preferences live in `~/.claude/CLAUDE.md` and apply here.
Project-specific additions:

- Update `DECISIONS.md` whenever a real trade-off is made. Prompt me if I forget.
- Deliberate failure testing is part of the project, not a distraction. When I
  break something on purpose, help me read the error rather than just fixing it.
- Remind me to commit at natural checkpoints — end of a verified build-order
  step, after a schema change, before starting something risky. Not after
  every small edit.
- Update `LEARNING.md` (private, gitignored) whenever a new technical
  concept gets explained — a few plain-language lines, not a transcript.
  It's my study aid for remembering this well enough later.
