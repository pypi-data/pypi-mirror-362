import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def _touch_healthcheck_file(filepath: Path, log_prefix: str):
    """
    Creates the parent directory if it doesn't exist and touches the healthcheck file.
    This is the core I/O operation for the heartbeat.

    Args:
        filepath: The Path object representing the file to touch.
        log_prefix: A prefix string (e.g., "Thread", "Gevent") for logging.
    """
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.touch()
        logger.debug(f"[{log_prefix}] Heartbeat: Touched {filepath}")
    except OSError as e:
        logger.error(f"[{log_prefix}] Heartbeat: FAILED to touch {filepath}: {e}")
