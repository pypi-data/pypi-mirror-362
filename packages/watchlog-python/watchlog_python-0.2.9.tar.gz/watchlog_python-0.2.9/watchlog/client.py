# watchlog.py

import os
import socket
import threading
from pathlib import Path
from typing import Union

import requests

# module‐level caches
_cached_server_url: str = None
_is_k8s: bool = None

def _is_running_in_k8s() -> bool:
    global _is_k8s
    if _is_k8s is not None:
        return _is_k8s

    # روش سریع: متغیر محیطی
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        _is_k8s = True
        return _is_k8s

    # ServiceAccount Token
    token = Path('/var/run/secrets/kubernetes.io/serviceaccount/token')
    if token.exists():
        _is_k8s = True
        return _is_k8s

    # cgroup
    try:
        with open('/proc/1/cgroup') as f:
            if 'kubepods' in f.read():
                _is_k8s = True
                return _is_k8s
    except Exception:
        pass

    # DNS lookup
    try:
        socket.gethostbyname('kubernetes.default.svc.cluster.local')
        _is_k8s = True
    except Exception:
        _is_k8s = False

    return _is_k8s

def _get_server_url() -> str:
    global _cached_server_url
    if _cached_server_url:
        return _cached_server_url

    # allow override via env
    override = os.getenv('WATCHLOG_AGENT_URL')
    if override:
        _cached_server_url = override.rstrip('/')
    else:
        host = (
            'watchlog-node-agent.monitoring.svc.cluster.local'
            if _is_running_in_k8s()
            else '127.0.0.1'
        )
        _cached_server_url = f'http://{host}:3774'

    return _cached_server_url

class Watchlog:
    def __init__(self, url: str = None):
        """
        url: optional override of the agent URL.
        If not provided, will auto-detect or use WATCHLOG_AGENT_URL.
        """
        self.base_url = (url or _get_server_url()).rstrip('/')

    def _request(self, full_url: str) -> None:
        try:
            requests.get(full_url, timeout=1)
        except Exception:
            # silent failure
            pass

    def _send_metric(self, method: str, metric: str, value: Union[int, float]) -> None:
        if not isinstance(metric, str) or not metric:
            return
        if not isinstance(value, (int, float)):
            return

        qs = {
            'method': method,
            'metric': metric,
            'value': value
        }
        url = f"{self.base_url}?{requests.utils.requote_uri(requests.compat.urlencode(qs))}"
        # fire-and-forget
        threading.Thread(target=self._request, args=(url,), daemon=True).start()

    def increment(self, metric: str, value: Union[int, float] = 1) -> None:
        if value > 0:
            self._send_metric('increment', metric, value)

    def decrement(self, metric: str, value: Union[int, float] = 1) -> None:
        if value > 0:
            self._send_metric('decrement', metric, value)

    def distribution(self, metric: str, value: Union[int, float]) -> None:
        self._send_metric('distribution', metric, value)

    def gauge(self, metric: str, value: Union[int, float]) -> None:
        self._send_metric('gauge', metric, value)

    def percentage(self, metric: str, value: Union[int, float]) -> None:
        if 0 <= value <= 100:
            self._send_metric('percentage', metric, value)

    def systembyte(self, metric: str, value: Union[int, float]) -> None:
        if value > 0:
            self._send_metric('systembyte', metric, value)


# singleton instance, like the Node.js module.exports = new SocketCli();
watchlog = Watchlog()
