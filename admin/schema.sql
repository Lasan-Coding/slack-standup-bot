CREATE TABLE members (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slack_user_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    timezone TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    last_prompted_date DATE
);

CREATE TABLE responses (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    member_id BIGINT NOT NULL REFERENCES members(id),
    standup_date DATE NOT NULL,
    yesterday TEXT,
    today TEXT,
    blockers TEXT,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (member_id, standup_date)
);

CREATE TABLE digest_log (
    posted_date DATE PRIMARY KEY
);
