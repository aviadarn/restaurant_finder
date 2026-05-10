# Reservation Hunter AI

Reservation Hunter AI is a production-oriented starter implementation for an MCP-compatible AI agent that monitors restaurant reservation platforms, ranks opportunities, joins waitlists, and books reservations with configurable human approval.

> Source context: NYC RSVPs is used as an inspiration source for restaurant release-timing metadata. It describes itself as a reference guide for popular NYC restaurant reservation release schedules and notes that restaurant schedules change regularly, so this project treats release timing as advisory metadata rather than a guaranteed truth source.

## Architecture

The application is split into clear service boundaries:

- **FastAPI backend** for user preferences, active searches, automation controls, booking history, cancellations, notifications, and health checks.
- **MCP layer** exposing tool-compatible functions for reservation search, waitlist joining, booking, cancellation, notifications, login/session state, browser snapshots, and retry recovery.
- **Agent layer** with planner, browser execution, reservation scoring, retry recovery, notification, and LangGraph-compatible orchestration boundaries.
- **Provider adapters** for Resy, OpenTable, Tock, SevenRooms, Yelp Reservations, and dynamically discovered providers.
- **Browser automation layer** using Playwright persistent browser contexts for session reuse and manual verification handoff.
- **Persistence layer** using PostgreSQL, SQLAlchemy 2 async models, Alembic migrations, Redis-ready workers, encrypted session blobs, and audit logs.
- **Deployment layer** with Docker Compose and Kubernetes starter manifests.

## Safety and compliance posture

This scaffold intentionally does **not** implement CAPTCHA bypass, fingerprint evasion, or deceptive anti-bot circumvention. Instead, it provides:

- persistent user-authorized browser sessions,
- provider-specific rate limits,
- randomized human-like pacing for normal form interactions,
- challenge detection hooks that route to human verification,
- encrypted session-token storage,
- audit logs,
- duplicate-booking prevention,
- human approval mode by default.

Before production use, review each provider's terms of service and prefer official APIs or approved partner integrations where available.

## File tree

```text
.
├── Dockerfile
├── README.md
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/0001_initial_schema.py
├── app/
│   ├── main.py
│   ├── agents/
│   │   ├── browser_executor.py
│   │   ├── graph.py
│   │   ├── notifier.py
│   │   ├── planner.py
│   │   ├── retry_recovery.py
│   │   └── scorer.py
│   ├── api/
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── automation.py
│   │       ├── bookings.py
│   │       ├── health.py
│   │       ├── notifications.py
│   │       ├── preferences.py
│   │       ├── searches.py
│   │       └── targets.py
│   ├── browser/
│   │   ├── captcha.py
│   │   ├── human_input.py
│   │   ├── manager.py
│   │   ├── snapshots.py
│   │   └── providers/
│   ├── core/
│   ├── db/
│   ├── mcp/
│   ├── services/
│   └── workers/
├── docker-compose.yml
├── infra/k8s/
├── pyproject.toml
└── tests/
```

## Core user inputs

Reservation targets support:

- preferred restaurant name,
- date range,
- time range,
- party size,
- neighborhoods,
- cuisines,
- priority,
- maximum acceptable time deviation,
- auto-book enabled/disabled,
- human approval requirement,
- notification preferences.

## Agent loop

A production scheduler or worker should repeatedly:

1. Load active `reservation_targets`.
2. Resolve known or dynamically discovered providers.
3. Call `ReservationGraph.run_once`.
4. Search provider adapters.
5. Score opportunities with `ReservationScoringAgent`.
6. Decide with `PlannerAgent` whether to wait, request approval, book, or join a waitlist.
7. Execute via `BrowserExecutionAgent`.
8. Persist booking attempts, waitlists, bookings, notifications, and audit events.
9. Back off intelligently during failures and respect provider rate limits.

## MCP tools

The tool module exposes async Python functions for:

- `search_reservations`
- `join_waitlist`
- `make_booking`
- `cancel_booking`
- `get_user_preferences`
- `notify_user`
- `login_provider`
- `session_manager`
- `anti_bot_manager`
- `browser_snapshot`
- `retry_failed_booking`

`app/mcp/server.py` provides a FastMCP entry point and can be extended to bind the database-backed tools to a running MCP transport.

## FastAPI endpoints

- `POST /targets` — create reservation target
- `PATCH /preferences` — update user preferences
- `POST /automation/pause` — pause active targets
- `POST /automation/resume` — resume paused targets
- `POST /bookings/{booking_id}/cancel` — cancel booking
- `GET /searches/active` — get active searches
- `GET /bookings/history` — get booking history
- `GET /notifications` — get notifications
- `GET /health` — health check

## Database schema

The initial Alembic migration creates:

- `users`
- `restaurants`
- `reservation_targets`
- `bookings`
- `waitlists`
- `sessions`
- `notifications`
- `provider_accounts`
- `booking_attempts`
- `audit_logs`

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
playwright install chromium
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Docker development

```bash
docker compose up --build
```

## Environment variables

See `.env.example` for database, Redis, OpenAI, encryption, notification, Playwright, and automation flags.

## Production recommendations

- Use managed PostgreSQL with PITR backups.
- Use managed Redis or a highly available Redis deployment.
- Store secrets in a cloud secret manager, not environment files.
- Rotate `SESSION_ENCRYPTION_KEY` with a versioned keyring design.
- Run Playwright workers in isolated containers with limited privileges.
- Add API authentication middleware and per-user authorization before exposing publicly.
- Add OpenTelemetry traces and metrics around scans, provider calls, and booking attempts.
- Keep auto-book disabled until provider compliance and billing/authorization flows are reviewed.
- Use human approval for high-value or ambiguous reservations.

## Scalability considerations

- Partition scan workloads by provider and release window.
- Use Redis leases to prevent duplicate scans.
- Persist booking attempt idempotency keys.
- Increase worker count only within provider-specific rate limits.
- Cache restaurant/provider metadata and refresh release windows periodically.
- Send notifications asynchronously so booking attempts are not blocked by SMS/email outages.

## Example flow

1. A user creates a target for `Via Carota`, party of 2, June 1-3, 7-8 PM.
2. The scan worker queries Resy/OpenTable/Tock/SevenRooms/Yelp adapters.
3. The scoring agent ranks a 7:30 PM Resy slot highly.
4. The planner requests approval unless the target has auto-book enabled and human approval disabled.
5. The booking service prevents duplicate active bookings for the same provider, restaurant, and time.
6. The notification service queues a success, approval-needed, waitlist, failure, or session-expiry alert.

## Future improvements

- Add first-class OpenAI Agents SDK model calls for ambiguous restaurant resolution and desirability inference.
- Wrap `ReservationGraph` with a durable LangGraph `StateGraph` runtime.
- Add official-provider API clients where available.
- Add browser-recorder assisted selector discovery with reviewed selector registries.
- Add release-window learning from historical booking success rates.
- Add WebAuthn/passkey-aware manual login handoff.
- Add multi-tenant API auth, roles, and admin dashboards.
