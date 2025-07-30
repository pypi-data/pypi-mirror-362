import logging
from pathlib import Path

from celery_pulse.executors import ThreadedHeartbeat

logger = logging.getLogger(__name__)

# A global variable to hold the manager instance for the beat process.
_beat_heartbeat_manager = None


def _on_beat_init(sender, **kwargs):
    """
    Signal handler for beat process initialization.
    Since beat doesn't use worker bootsteps, it needs its own mechanism.
    """
    global _beat_heartbeat_manager
    logger.info(
        "Heartbeat: beat_init signal received. Starting heartbeat for beat process."
    )

    app_conf = sender.app.conf
    interval = app_conf.get("pulse_heartbeat_interval", 60)
    filepath = Path(
        app_conf.get("pulse_healthcheck_file", "/tmp/celery_health_beat.txt")
    )

    _beat_heartbeat_manager = ThreadedHeartbeat(filepath, interval)
    _beat_heartbeat_manager.start()
