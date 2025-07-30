import logging
import os
from pathlib import Path

from celery import bootsteps

from celery_pulse.executors import GeventHeartbeat, ThreadedHeartbeat

try:
    from gevent.event import Event as GeventEvent
except ImportError:
    GeventEvent = None

logger = logging.getLogger(__name__)


class HeartbeatBootstep(bootsteps.StartStopStep):
    """
    A universal Celery bootstep that starts a heartbeat mechanism within a worker.
    It intelligently selects the correct executor (thread or greenlet) based on
    the worker's pool type, ensuring an accurate health check.
    """

    def __init__(self, worker, **kwargs):
        super().__init__(worker, **kwargs)
        self.manager = None
        pool_cls = getattr(worker.pool, "__class__", None)
        pool_name = getattr(pool_cls, "__name__", "").lower()
        self.is_gevent = "gevent" in pool_name

    def start(self, worker):
        """Called when the worker process starts."""
        logger.info(
            f"Heartbeat: Bootstep starting in PID {os.getpid()}. "
            f"Pool is {'gevent' if self.is_gevent else 'prefork/solo'}."
        )
        interval = worker.app.conf.get("pulse_heartbeat_interval", 60)
        filepath = Path(
            worker.app.conf.get("pulse_healthcheck_file", "/tmp/celery_health.txt")
        )

        if self.is_gevent and GeventEvent:
            self.manager = GeventHeartbeat(filepath, interval)
        else:
            self.manager = ThreadedHeartbeat(filepath, interval)

        self.manager.start()

    def stop(self, worker):
        """Called when the worker process shuts down."""
        logger.info(f"Heartbeat: Bootstep stopping in PID {os.getpid()}.")

        if self.manager:
            self.manager.stop()
