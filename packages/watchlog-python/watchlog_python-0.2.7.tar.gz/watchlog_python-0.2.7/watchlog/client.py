import os
import socket
import threading
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Union

def _is_running_in_k8s() -> bool:
    # روش سریع: متغیر محیطی
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        return True

    # روش 1: ServiceAccount Token
    token_path = Path('/var/run/secrets/kubernetes.io/serviceaccount/token')
    if token_path.exists():
        return True

    # روش 2: بررسی cgroup
    try:
        with open('/proc/1/cgroup') as f:
            if 'kubepods' in f.read():
                return True
    except Exception:
        pass

    # روش 3: DNS lookup
    try:
        socket.gethostbyname('kubernetes.default.svc.cluster.local')
        return True
    except Exception:
        return False

def _detect_agent_url() -> str:
    # اولویت 1: اگر خودِ کاربر URL را override کرده
    override = os.getenv('WATCHLOG_AGENT_URL')
    if override:
        return override.rstrip('/')

    # اولویت 2: تشخیص خودکار
    if _is_running_in_k8s():
        # سرویس داخل namespace monitoring
        host = 'watchlog-node-agent.monitoring.svc.cluster.local'
    else:
        host = 'localhost'
    return f'http://{host}:3774'

class Watchlog:
    def __init__(self, url: str = None):
        """
        اگر پارامتر url داده شده، از آن استفاده می‌کند،
        در غیر این صورت اول env.override، بعد detection خودکار.
        """
        self.url = (url or _detect_agent_url()).rstrip('/')

    def send_metric(self, method: str, metric: str, value: Union[int, float] = 1) -> None:
        # فقط مقادیر عددی و متریک‌های غیراخالی
        if not isinstance(value, (int, float)) or not metric:
            return

        def _send():
            qs = urllib.parse.urlencode({
                "method": method,
                "metric": metric,
                "value": value
            })
            full_url = f"{self.url}?{qs}"
            try:
                urllib.request.urlopen(full_url, timeout=1)
            except Exception:
                # silent fail
                pass

        threading.Thread(target=_send, daemon=True).start()

    def increment(self, metric: str, value: Union[int, float] = 1) -> None:
        if value > 0:
            self.send_metric('increment', metric, value)

    def decrement(self, metric: str, value: Union[int, float] = 1) -> None:
        if value > 0:
            self.send_metric('decrement', metric, value)

    def gauge(self, metric: str, value: Union[int, float]) -> None:
        self.send_metric('gauge', metric, value)

    def percentage(self, metric: str, value: Union[int, float]) -> None:
        if 0 <= value <= 100:
            self.send_metric('percentage', metric, value)

    def systembyte(self, metric: str, value: Union[int, float]) -> None:
        if value > 0:
            self.send_metric('systembyte', metric, value)
