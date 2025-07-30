import time
import threading
import socket
from pathlib import Path
import requests
from .collector import flush

# ---- تشخیص محیط Kubernetes در سه گام (و کش کردن نتیجه) ----
def is_running_in_k8s() -> bool:
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

def detect_agent_url() -> str:
    if detect_agent_url._cached is None:
        in_k8s = is_running_in_k8s()
        detect_agent_url._cached = (
            'http://watchlog-node-agent.monitoring.svc.cluster.local:3774/apm'
            if in_k8s
            else 'http://localhost:3774/apm'
        )
    return detect_agent_url._cached

detect_agent_url._cached = None

# ---- راه‌اندازی Session برای keep-alive و header مشترک ----
_session = requests.Session()
_session.headers.update({'Content-Type': 'application/json'})
_agent_url = detect_agent_url()

_interval_seconds = 10

def _send(metrics):
    if not metrics:
        return

    payload = {
        "collected_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "platformName": "flask",
        "metrics": metrics,
    }

    try:
        _session.post(_agent_url, json=payload, timeout=3)
    except Exception:
        # فیلد خطا به‌طور silent نادیده گرفته می‌شود
        pass

def start():
    """
    استارت کردن حلقه‌ی ارسال:
    هر `_interval_seconds` ثانیه، متریک‌ها flush می‌شوند و در صورت وجود،
    به آژنت ارسال می‌شوند.
    """
    def _loop():
        while True:
            try:
                metrics = flush()
                if metrics:
                    _send(metrics)
            except Exception:
                pass
            time.sleep(_interval_seconds)

    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
