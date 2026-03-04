from __future__ import annotations
import os
from typing import Any, Dict, List, Optional
import requests

class MLTrackClient:
    def __init__(self, base_url: Optional[str] = None, timeout_s: float = 10.0) -> None:
        self.base_url = (base_url or os.getenv("MLTRACK_BASE_URL", "http://127.0.0.1:8000")).rstrip("/")
        self.timeout_s = timeout_s

    def _url(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return f"{self.base_url}{path}"

    def post(self, path: str, json_body: Any) -> Any:
        resp = requests.post(self._url(path), json=json_body, timeout=self.timeout_s)
        resp.raise_for_status()
        return resp.json()

    def get(self, path: str) -> Any:
        resp = requests.get(self._url(path), timeout=self.timeout_s)
        resp.raise_for_status()
        return resp.json()

    def create_run(self, project: str, experiment: str, name: str) -> Dict[str, Any]:
        return self.post("/api/runs", {"project": project, "experiment": experiment, "name": name})

    def upsert_params(self, run_id: int, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        items = [{"key": k, "value": v} for k, v in params.items()]
        return self.post(f"/api/runs/{run_id}/params", items)

    def log_metrics(self, run_id: int, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.post(f"/api/runs/{run_id}/metrics", metrics)

    def patch(self, path: str, json_body: Any) -> Any:
        resp = requests.patch(self._url(path), json=json_body, timeout=self.timeout_s)
        resp.raise_for_status()
        return resp.json()

    def update_run(self, run_id: int, status: str) -> Dict[str, Any]:
        return self.patch(f"/api/runs/{run_id}", {"status": status})