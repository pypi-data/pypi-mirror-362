import threading
import urllib.parse
import urllib.request
import os
from pathlib import Path
import socket
import logging

# تنظیم logger
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("watchlog")

def is_running_in_k8s() -> bool:
    logger.debug("Checking if running inside Kubernetes...")
    # Method 1: ServiceAccount Token
    token_path = Path('/var/run/secrets/kubernetes.io/serviceaccount/token')
    if token_path.exists():
        logger.debug("Found Kubernetes serviceaccount token at %s", token_path)
        return True
    # Method 2: cgroup
    try:
        with open('/proc/1/cgroup') as f:
            content = f.read()
            if 'kubepods' in content:
                logger.debug("Found 'kubepods' in /proc/1/cgroup")
                return True
    except Exception as e:
        logger.warning("Error reading /proc/1/cgroup: %s", e)
    # Method 3: DNS lookup
    try:
        socket.gethostbyname('kubernetes.default.svc.cluster.local')
        logger.debug("DNS lookup for kubernetes.default.svc.cluster.local succeeded")
        return True
    except socket.gaierror:
        logger.debug("DNS lookup failed, not in k8s")
    return False

def detect_default_url() -> str:
    if is_running_in_k8s():
        url = 'http://watchlog-node-agent:3774'
        logger.info("Detected Kubernetes environment, using URL %s", url)
    else:
        url = 'http://localhost:3774'
        logger.info("Non-Kubernetes environment, using URL %s", url)
    return url

class Watchlog:
    def __init__(self, url: str = None):
        """
        Initialize Watchlog client.
        If url is provided, use it; otherwise, detect the default URL.
        """
        self.url = url or detect_default_url()
        logger.info("Watchlog initialized with URL: %s", self.url)

    def send_metric(self, method, metric, value=1):
        # Only send numeric values
        if not isinstance(value, (int, float, complex)):
            logger.error("Value %r for metric %s is not numeric, skipping send", value, metric)
            return

        def _send():
            params = urllib.parse.urlencode({
                "method": method,
                "metric": metric,
                "value": value
            })
            full_url = f"{self.url}?{params}"
            logger.debug("Sending metric: method=%s metric=%s value=%s to URL=%s",
                         method, metric, value, full_url)
            try:
                req = urllib.request.Request(full_url)
                with urllib.request.urlopen(req, timeout=1) as resp:
                    logger.info("Metric sent successfully, status code: %s", resp.getcode())
            except Exception as e:
                logger.error("Failed to send metric to %s: %s", full_url, e)

        # Use a daemon thread to avoid blocking
        logger.debug("Spawning thread to send metric %s", metric)
        threading.Thread(target=_send, daemon=True).start()

    def increment(self, metric, value=1):
        """Increment a counter by the given value."""
        logger.debug("increment called with metric=%s, value=%s", metric, value)
        self.send_metric('increment', metric, value)

    def decrement(self, metric, value=1):
        """Decrement a counter by the given value."""
        logger.debug("decrement called with metric=%s, value=%s", metric, value)
        self.send_metric('decrement', metric, value)

    def gauge(self, metric, value):
        """Record the current value of a gauge."""
        logger.debug("gauge called with metric=%s, value=%s", metric, value)
        self.send_metric('gauge', metric, value)

    def percentage(self, metric, value):
        """Record a percentage value (0-100)."""
        logger.debug("percentage called with metric=%s, value=%s", metric, value)
        if 0 <= value <= 100:
            self.send_metric('percentage', metric, value)
        else:
            logger.error("Percentage value %s out of range [0,100], skipping", value)

    def systembyte(self, metric, value):
        """Record a system byte metric."""
        logger.debug("systembyte called with metric=%s, value=%s", metric, value)
        self.send_metric('systembyte', metric, value)
