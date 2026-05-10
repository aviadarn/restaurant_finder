"""OpenAI Agents SDK orchestration definitions.

Deployments with `openai-agents` installed can import `reservation_planner_agent`
and connect it to the database-backed MCP tools. The core service layer remains
framework-independent so queue workers, MCP transports, and FastAPI endpoints can
share the same business logic.
"""
from agents import Agent

reservation_planner_agent = Agent(
    name="Reservation Hunter Planner",
    instructions=(
        "Rank restaurant reservation opportunities using the user's restaurant, date, "
        "time, party size, cuisine, neighborhood, priority, approval, and auto-book "
        "constraints. Prefer official/provider-compliant actions, avoid duplicate "
        "bookings, request human approval when required, and route CAPTCHA or login "
        "challenges to manual verification."
    ),
)

browser_execution_agent = Agent(
    name="Reservation Hunter Browser Executor",
    instructions=(
        "Execute approved provider actions through Playwright adapters, preserving "
        "authorized sessions and stopping for human verification challenges."
    ),
)

notification_agent = Agent(
    name="Reservation Hunter Notification Agent",
    instructions="Send concise booking, waitlist, failure, and session-health notifications.",
)
