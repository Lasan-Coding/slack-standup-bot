# Decisions Log

## 2026-08-12 — Membership stays admin-only, not self-service
Considered letting members add/remove themselves instead of an admin-run
CLI script. Self-service is arguably the better design for many teams.
Kept admin-only anyway — it matches the scope as originally written, and
avoids extra complexity (who can add/remove whom, any approval flow).
Revisit if the project's scope changes.
