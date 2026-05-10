from app.workers.celery_app import celery_app


@celery_app.task(name="reservation_hunter.scan_targets")
def scan_targets() -> dict:
    return {"status": "queued", "message": "Async scan loop should be launched by deployment scheduler"}
