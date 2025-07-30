# Celery Pulse

[![PyPI version](https://badge.fury.io/py/celery-pulse.svg)](https://badge.fury.io/py/celery-pulse)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/celery-pulse)

A simple, framework-agnostic heartbeat mechanism for Celery.

`celery-pulse` helps you monitor the true health of your Celery workers and beat scheduler. A common problem with Celery monitoring is that a worker process can be running but "stuck" or frozen, unable to process tasks. Standard health checks that just check if the process exists will report a false positive.

This library solves the problem by running a lightweight background thread (or greenlet) inside each Celery worker process and the beat process. This thread's only job is to periodically "touch" a healthcheck file. If the file's modification timestamp is not recent, it means the process is unresponsive, allowing you to take action.

## Key Features

-   **Framework-Agnostic:** Works with Django, Flask, FastAPI, or any other Python application.
-   **Smart Pool Detection:** Automatically uses the correct concurrency primitive:
    -   `gevent`: A non-blocking greenlet via a Celery bootstep.
    -   `prefork`/`solo`: A standard background thread via Celery signals.
-   **Beat Support:** Monitors the `celery beat` scheduler process in addition to workers.
-   **Lightweight & Safe:** The heartbeat runs in a separate thread/greenlet and won't block your tasks.
-   **Simple Integration:** Requires only a one-line function call to set up.
-   **Easy to Monitor:** Compatible with any monitoring system that can check a file's timestamp (Docker `HEALTHCHECK`, Kubernetes `livenessProbe`, etc.).

## Installation

```bash
pip install celery-pulse
```

If you are using the `gevent` worker pool, you can install the required dependency as an extra:
```bash
pip install celery-pulse[gevent]
```

## Quick Start

The only step is to import and call `init_celery_pulse()` with your Celery app instance after it has been configured.

### Example: Standalone Celery (Flask, FastAPI, etc.)

In your Celery app file (e.g., `tasks.py`):

```python
# tasks.py
from celery import Celery
from celery_pulse import init_celery_pulse

app = Celery('my_tasks', broker='redis://localhost:6379/0')

# Configure celery-pulse settings directly in Celery's config
app.conf.update(
    pulse_heartbeat_interval=30,  # Heartbeat every 30 seconds
    pulse_healthcheck_file="/var/run/celery_health.txt"  # Path to the heartbeat file
)

# Initialize the heartbeat mechanism
init_celery_pulse(app)

# --- Define your tasks as usual ---
@app.task
def add(x, y):
    return x + y
```

### Example: Django Integration

In your project's `celery.py` file:

```python
# myproject/celery.py
import os
from celery import Celery
from celery_pulse import init_celery_pulse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Use a namespace for all Celery-related settings in django's settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Initialize the heartbeat mechanism
# It will read its configuration from your Django settings
init_celery_pulse(app)

app.autodiscover_tasks()
```

Then, configure the settings in your `myproject/settings.py`:

```python
# myproject/settings.py

# ... your other Django settings

# Celery settings
CELERY_BROKER_URL = "redis://localhost:6379/0"
# ... other celery settings

# Celery Pulse settings (must use the CELERY_ namespace)
CELERY_PULSE_HEARTBEAT_INTERVAL = 30
CELERY_PULSE_HEALTHCHECK_FILE = "/var/run/myproject/celery_health.txt"
```

## Configuration

`celery-pulse` is configured through your Celery application's configuration.

| Parameter | `app.conf` key | Django `settings.py` key | Description | Default |
| :--- | :--- | :--- | :--- | :--- |
| **Interval** | `pulse_heartbeat_interval` | `CELERY_PULSE_HEARTBEAT_INTERVAL` | The interval in seconds at which the heartbeat file is touched. | `60` |
| **File Path** | `pulse_healthcheck_file` | `CELERY_PULSE_HEALTHCHECK_FILE` | The absolute path to the healthcheck file that will be created and updated. | `"/tmp/celery_healthcheck"` |

## How to Use the Healthcheck File

Once `celery-pulse` is running, it will update the specified file every `pulse_heartbeat_interval` seconds. Your monitoring system should check if the file's last modification time is recent.

A good rule of thumb is to fail the health check if the file hasn't been updated in `2 * pulse_heartbeat_interval` seconds. This provides a safe margin for delays.

### Example: Docker `HEALTHCHECK`

In your `Dockerfile`, you can add a health check that verifies the file was modified within the last 65 seconds (assuming a 30-second interval).

```dockerfile
# Assuming pulse_heartbeat_interval = 30
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD [ -f /var/run/celery_health.txt ] && [ $(($(date +%s) - $(stat -c %Y /var/run/celery_health.txt))) -lt 65 ] || exit 1
```
*   `[ -f ... ]`: Checks if the file exists.
*   `$(($(date +%s) - $(stat -c %Y ...)))`: Calculates the age of the file in seconds.
*   `-lt 65`: Checks if the age is less than 65 seconds.

### Example: Kubernetes `livenessProbe`

In your Kubernetes deployment YAML, you can add a `livenessProbe` to automatically restart a pod if its worker becomes unresponsive.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-worker
spec:
  # ...
  template:
    # ...
    spec:
      containers:
      - name: worker
        image: my-celery-app:latest
        command: ["celery", "-A", "myproject", "worker", "-l", "info"]
        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - "[ -f /var/run/celery_health.txt ] && [ $(($(date +%s) - $(stat -c %Y /var/run/celery_health.txt))) -lt 65 ]"
          initialDelaySeconds: 60 # Give time for the worker to start
          periodSeconds: 30       # Check every 30 seconds
          failureThreshold: 2     # Fail after 2 consecutive failures
```

## How It Works

`celery-pulse` intelligently adapts to the Celery execution environment:

1.  **Gevent Pool**: If `gevent` is detected as the worker pool, `celery-pulse` registers a Celery `bootstep`. This starts a dedicated, non-blocking **greenlet** that runs the heartbeat loop. This is the most efficient method for `gevent`.
2.  **Prefork/Solo Pool & Beat**: For the default `prefork` pool, the `solo` pool, and the `celery beat` scheduler, the library connects to Celery's startup signals (`worker_process_init`, `beat_init`). When a process starts, it launches a standard Python **thread** to manage the heartbeat. The thread is gracefully stopped on shutdown.
3.  **Pool Detection**: The library uses the `on_after_configure` signal to inspect the configured `worker_pool` and sets an environment variable. This variable is inherited by forked worker processes, allowing them to know which heartbeat strategy to use.

## Contributing

Contributions are welcome! If you find a bug or have an idea for an improvement, please open an issue or submit a pull request on our [GitHub repository](https://github.com/yourusername/celery-pulse).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
