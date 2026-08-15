# Decisions Log

## 2026-08-12 – Membership stays admin-only, not self-service
Considered letting members add/remove themselves instead of an admin-run
CLI script. Self-service is arguably the better design for many teams.
Kept admin-only anyway – it matches the scope as originally written, and
avoids extra complexity (who can add/remove whom, any approval flow).
Revisit if the project's scope changes.

## 2026-08-12 – Digest anchored to one timezone, not built for globally distributed teams
A single fixed digest time only works when a team's timezones are reasonably
close together – for teams spread across very different zones, some members'
own morning wouldn't have arrived yet by digest time, incorrectly showing
them as non-responders. Considered solving this and decided against it – not
what this project needs to prove. Geekbot avoids the problem differently: it
posts each answer to the channel as it comes in, rather than batching into
one digest ([Daily Sync](https://help.geekbot.com/en/articles/7041480-daily-sync),
[personalizing standup settings](https://help.geekbot.com/en/articles/4311783-how-to-personalize-your-standup-settings)) –
a different product shape than what's scoped here, and arguably the better solution. Per-member timezone-aware
prompting is unaffected and still fully built; only the digest's single post
time carries this limitation.

## 2026-08-13 – Real deployment deferred to a future iteration
Free hosting for a persistent, always-on process doesn't fit this project's
current constraints – revisit later, possibly self-hosted.

## 2026-08-15 – Oracle Cloud attempt abandoned; deployment stays deferred, Docker/CI added anyway
Oracle was the only host found offering a persistent free VM with no
ongoing cost. Its signup
process failed repeatedly with a generic, unresolvable "unable to
complete your sign up" error – a known issue on Oracle's side with no
documented fix. Rather than continue troubleshooting a third-party black
box indefinitely, decided to stop and focus on the parts of the goal that
were still fully achievable.

Containerized the app with Docker and added CI (GitHub Actions builds and
publishes the image to GitHub Container Registry on push to `main`) –
both real, verifiable skills independent of hosting. Live hosting stays
deferred; the
two paths to close it out later are a low-cost VPS (a few
euros/month, no free-tier friction) or going with a time-boxed free trial.
