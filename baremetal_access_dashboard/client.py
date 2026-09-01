from urllib.parse import urljoin

import requests
from django.conf import settings


class AccessAPIError(RuntimeError):
    pass


def request(user, method: str, path: str, *, json=None, idempotency_key: str | None = None):
    base = getattr(settings, "BAREMETAL_ACCESS_API_URL", "")
    if not base.startswith(("http://", "https://")):
        raise AccessAPIError("Bare Metal Access API is not configured")
    token = getattr(user, "token", None)
    if not token:
        raise AccessAPIError("A project-scoped OpenStack token is required")
    token = getattr(token, "id", token)
    if not isinstance(token, (str, bytes)) or not token:
        raise AccessAPIError("A project-scoped OpenStack token is required")
    headers = {"X-Auth-Token": token, "Accept": "application/json"}
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    response = requests.request(
        method, urljoin(base.rstrip("/") + "/", path.lstrip("/")), json=json,
        headers=headers, timeout=(3.05, 30),
    )
    content_type = response.headers.get("Content-Type", "")
    if response.status_code >= 400 or "application/json" not in content_type:
        raise AccessAPIError(f"Access API returned {response.status_code}")
    return response.json()
