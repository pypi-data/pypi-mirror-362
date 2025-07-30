import logging

from celery import Celery
from celery.signals import beat_init

from .beat import _on_beat_init
from .bootstep import HeartbeatBootstep

__all__ = ["init_celery_pulse"]

logger = logging.getLogger(__name__)


def init_celery_pulse(app: Celery):
    """
    Initializes the celery-pulse heartbeat mechanism for a Celery application.

    This function hooks into the Celery lifecycle by:
    1. Adding a custom bootstep to all workers (prefork, gevent, solo).
    2. Connecting a signal handler for the celery beat scheduler.

    Args:
        app: The Celery application instance.
    """
    logger.info(
        "Heartbeat: Initializing celery-pulse. Adding bootsteps and connecting signals."
    )

    # 1. Add the bootstep for all worker types.
    app.steps["worker"].add(HeartbeatBootstep)

    # 2. Connect the separate signal handler for the beat scheduler.
    beat_init.connect(_on_beat_init)
