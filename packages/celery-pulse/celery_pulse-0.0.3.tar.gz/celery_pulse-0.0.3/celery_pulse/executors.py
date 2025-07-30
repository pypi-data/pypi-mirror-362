import logging
from pathlib import Path
from threading import Event, Thread

from celery_pulse.utils import _touch_healthcheck_file

try:
    from gevent import sleep, spawn
    from gevent.event import Event as GeventEvent
except ImportError:
    spawn = sleep = GeventEvent = None

logger = logging.getLogger(__name__)


class ThreadedHeartbeat:
    """
    A heartbeat executor that uses a standard Python thread.
    Ideal for prefork/solo pools and the beat scheduler.
    """

    def __init__(self, filepath: Path, interval: int):
        self._filepath, self._interval = filepath, interval
        self._thread, self._stop_event = None, Event()

    def start(self):
        """Starts the background heartbeat thread."""
        if self._thread and self._thread.is_alive():
            return

        logger.info("Heartbeat: Starting thread-based heartbeat...")

        self._stop_event.clear()
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stops the background heartbeat thread gracefully."""
        if not self._thread:
            return

        logger.info("Heartbeat: Stopping thread-based heartbeat...")
        self._stop_event.set()

        if self._thread.is_alive():
            self._thread.join(timeout=self._interval + 5)

    def _run(self):
        """The main loop for the heartbeat thread."""
        while not self._stop_event.is_set():
            _touch_healthcheck_file(self._filepath, "Thread")
            self._stop_event.wait(self._interval)


class GeventHeartbeat:
    """
    A heartbeat executor that uses a gevent greenlet.
    Ideal for gevent pools, as it integrates with the gevent event loop.
    """

    def __init__(self, filepath: Path, interval: int):
        if not GeventEvent:
            raise RuntimeError(
                "Gevent is not installed, but GeventHeartbeat was initiated."
            )

        self._filepath, self._interval = filepath, interval
        self._greenlet, self._stop_event = None, GeventEvent()

    def start(self):
        """Spawns the background heartbeat greenlet."""
        logger.info("Heartbeat: Starting gevent-based greenlet heartbeat...")
        self._greenlet = spawn(self.run)

    def stop(self):
        """Stops the background heartbeat greenlet gracefully."""
        logger.info("Heartbeat: Stopping gevent-based greenlet heartbeat...")
        self._stop_event.set()

        if self._greenlet:
            self._greenlet.join(timeout=self._interval + 5)

    def run(self):
        """The main loop for the heartbeat greenlet."""
        while not self._stop_event.is_set():
            _touch_healthcheck_file(self._filepath, "Gevent")
            sleep(self._interval)
