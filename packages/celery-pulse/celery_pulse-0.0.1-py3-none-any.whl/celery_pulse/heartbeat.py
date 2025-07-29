import logging
import os
from pathlib import Path
from threading import Thread, Event

from celery import Celery, bootsteps
from celery.signals import worker_process_init, worker_process_shutdown, beat_init

try:
    from gevent import spawn, sleep
    from gevent.event import Event as GeventEvent
except ImportError:
    spawn = sleep = GeventEvent = None

logger = logging.getLogger(__name__)


# --- Core Heartbeat Logic ---
def _touch_healthcheck_file(filepath: Path, log_prefix: str):
    """Creates the parent directory and touches the healthcheck file."""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.touch()
        logger.debug(f"[{log_prefix}] Heartbeat file {filepath} touched.")
    except (IOError, OSError) as e:
        logger.error(f"[{log_prefix}] Failed to write to heartbeat file {filepath}: {e}")


# --- Thread-based heartbeat ---
class ThreadedHeartbeat:
    """Manages the heartbeat for a process using a standard Python thread."""

    def __init__(self, filepath: Path, interval: int):
        self._filepath = filepath
        self._interval = interval
        self._thread = None
        self._stop_event = Event()

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        logger.info("Starting thread-based heartbeat...")
        self._stop_event.clear()
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        if not self._thread:
            return
        logger.info("Stopping thread-based heartbeat...")
        self._stop_event.set()
        if self._thread.is_alive():
            self._thread.join(timeout=self._interval + 5)
        self._thread = None

    def _run(self):
        while not self._stop_event.is_set():
            _touch_healthcheck_file(self._filepath, "Thread")
            self._stop_event.wait(self._interval)


# --- Gevent-based heartbeat ---
if GeventEvent:
    class GeventHeartbeat(bootsteps.StartStopStep):
        """Celery bootstep to manage a heartbeat for gevent workers."""
        requires = ('celery.worker.components.Timer',)

        def __init__(self, worker, **kwargs):
            self.filepath = Path(worker.app.conf.get("healthcheck_file", "/tmp/celery_healthcheck"))
            self.interval = worker.app.conf.get("heartbeat_interval", 60)
            self.t = None
            self.stop_event = GeventEvent()

        def start(self, worker):
            logger.info("Starting gevent-based heartbeat...")
            self.t = spawn(self.run)

        def stop(self, worker):
            logger.info("Stopping gevent-based heartbeat...")
            self.stop_event.set()
            if self.t:
                self.t.join(timeout=self.interval + 5)

        def run(self):
            while not self.stop_event.is_set():
                _touch_healthcheck_file(self.filepath, "Gevent")
                sleep(self.interval)


# --- Public Initialization Function ---

def init_celery_heartbeat(app: Celery):
    """
    Initializes and attaches the heartbeat mechanism to a Celery application.

    This function reads configuration from the Celery app instance and
    attaches the appropriate signal handlers and bootsteps.

    Configuration (read from app.conf):
    - `heartbeat_interval` (int): Interval in seconds. Defaults to 60.
    - `healthcheck_file` (str): Path to the healthcheck file. Defaults to '/tmp/celery_healthcheck'.
    """

    # Read config from Celery app, not Django settings
    interval = app.conf.get("heartbeat_interval", 60)
    filepath = Path(app.conf.get("healthcheck_file", "/tmp/celery_healthcheck"))

    # --- Attach Gevent Bootstep if available ---
    if GeventEvent:
        app.steps['worker'].add(GeventHeartbeat)

    # --- Signal Handlers (for prefork, solo, and beat) ---
    # Create a single instance of the manager for each process
    threaded_heartbeat_manager = ThreadedHeartbeat(filepath, interval)

    @app.on_after_configure.connect
    def set_pool_env_var(sender, **kwargs):
        pool_cls = sender.conf.worker_pool
        pool_name = pool_cls if isinstance(pool_cls, str) else getattr(pool_cls, '__name__', '')
        if 'gevent' in pool_name.lower():
            os.environ['CELERY_POOL_IMPL'] = 'gevent'
        else:
            os.environ['CELERY_POOL_IMPL'] = 'other'

    @beat_init.connect(sender=app)
    def on_beat_init(**kwargs):
        logger.info("Celery beat initialized. Starting heartbeat.")
        threaded_heartbeat_manager.start()

    @worker_process_init.connect(sender=app)
    def on_worker_init(**kwargs):
        is_gevent = os.environ.get('CELERY_POOL_IMPL') == 'gevent'
        if not is_gevent:
            logger.info("Non-gevent worker process initialized. Starting heartbeat.")
            threaded_heartbeat_manager.start()

    @worker_process_shutdown.connect(sender=app)
    def on_worker_shutdown(**kwargs):
        is_gevent = os.environ.get('CELERY_POOL_IMPL') == 'gevent'
        if not is_gevent:
            threaded_heartbeat_manager.stop()