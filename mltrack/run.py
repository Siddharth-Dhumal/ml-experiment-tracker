from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
from .client import MLTrackClient

@dataclass
class Run:
    id: int
    project: str
    experiment: str
    name: str
    client: MLTrackClient

    @classmethod
    def create(
        cls,
        project: str,
        experiment: str,
        name: str,
        *,
        base_url: Optional[str] = None,
        timeout_s: float = 10.0,
        params: Optional[Dict[str, Any]] = None,
    ) -> "Run":
        client = MLTrackClient(base_url=base_url, timeout_s=timeout_s)
        created = client.create_run(project=project, experiment=experiment, name=name)

        run = cls(
            id=int(created["id"]),
            project=str(created["project"]),
            experiment=str(created["experiment"]),
            name=str(created["name"]),
            client=client,
        )

        if params:
            run.log_params(params)

        return run

    def log_params(self, params: Dict[str, Any]) -> None:
        self.client.upsert_params(self.id, params)

    def log_metrics(self, metrics: Dict[str, float], *, step: int) -> None:
        items = [{"name": k, "value": float(v), "step": int(step)} for k, v in metrics.items()]
        self.client.log_metrics(self.id, items)