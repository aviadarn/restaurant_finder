from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import automation, bookings, health, notifications, preferences, searches, targets
from app.core.config import settings
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("app_start", app=settings.app_name, environment=settings.environment)
    yield
    logger.info("app_stop")


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.include_router(health.router)
app.include_router(targets.router)
app.include_router(preferences.router)
app.include_router(automation.router)
app.include_router(bookings.router)
app.include_router(searches.router)
app.include_router(notifications.router)
