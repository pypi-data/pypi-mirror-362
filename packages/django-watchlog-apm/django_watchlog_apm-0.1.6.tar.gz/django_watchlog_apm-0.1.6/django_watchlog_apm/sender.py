# django_watchlog_apm/sender.py
import json
import threading
import time
import socket
from pathlib import Path
import requests
from urllib.parse import urlparse
from .collector import flush

# ---- تشخیص اجرای داخل Kubernetes در سه مرحله و کش کردن نتیجه ----
def _is_running_in_k8s() -> bool:
    token_path = Path('/var/run/secrets/kubernetes.io/serviceaccount/token')
    if token_path.exists():
        return True

    try:
        with open('/proc/1/cgroup') as f:
            if 'kubepods' in f.read():
                return True
    except Exception:
        pass

    try:
        socket.gethostbyname('kubernetes.default.svc.cluster.local')
        return True
    except Exception:
        return False

def _detect_agent_url() -> str:
    if not hasattr(_detect_agent_url, "_cached"):
        in_k8s = _is_running_in_k8s()
        _detect_agent_url._cached = (
            'http://watchlog-node-agent.monitoring.svc.cluster.local:3774/apm'
            if in_k8s
            else 'http://localhost:3774/apm'
        )
    return _detect_agent_url._cached

# ---- یک Session با keep-alive برای بهبود کارایی ----
_session = requests.Session()
_session.headers.update({'Content-Type': 'application/json'})
_agent_url = _detect_agent_url()

def _send(data):
    if not data:
        return

    payload = {
        "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "platformName": "django",
        "metrics": data,
    }

    try:
        _session.post(_agent_url, json=payload, timeout=3)
    except Exception:
        # خطاها silent نادیده گرفته می‌شوند
        pass

def start(interval=10):
    """
    هر max(10, interval) ثانیه یک‌بار متریک‌ها flush و ارسال می‌شوند.
    """
    def _loop():
        while True:
            try:
                data = flush()
                if data:
                    _send(data)
            except Exception:
                pass
            time.sleep(max(10, interval))

    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
