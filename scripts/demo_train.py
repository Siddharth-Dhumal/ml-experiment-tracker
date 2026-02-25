import time
import random
import requests

BASE_URL = "http://127.0.0.1:8000"

def create_run(project: str, experiment: str, name: str) -> int:
    resp = requests.post(
        f"{BASE_URL}/api/runs",
        json={"project": project, "experiment": experiment, "name": name},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["id"]

def upsert_params(run_id: int, params: dict) -> None:
    payload = [{"key": k, "value": v} for k, v in params.items()]
    resp = requests.post(f"{BASE_URL}/api/runs/{run_id}/params", json=payload, timeout=10)
    resp.raise_for_status()

def log_metrics(run_id: int, items: list[dict]) -> None:
    resp = requests.post(f"{BASE_URL}/api/runs/{run_id}/metrics", json=items, timeout=10)
    resp.raise_for_status()

def main() -> None:
    run_id = create_run(project="demo", experiment="mnist", name="demo-train")
    print(f"Created run_id={run_id}")

    upsert_params(
        run_id,
        {
            "lr": 0.001,
            "batch_size": 64,
            "model": "mlp",
            "seed": 42,
        },
    )
    print("Logged params")

    loss = 1.2
    acc = 0.30

    for step in range(20):
        loss = max(0.05, loss * (0.90 + random.random() * 0.03))
        acc = min(0.99, acc + (0.02 + random.random() * 0.01))

        metrics_batch = [
            {"name": "loss", "value": loss, "step": step},
            {"name": "acc", "value": acc, "step": step},
        ]
        log_metrics(run_id, metrics_batch)
        print(f"step={step:02d} loss={loss:.4f} acc={acc:.4f}")

        time.sleep(0.2)

    print("Done. View in Swagger:")
    print(f"  {BASE_URL}/docs")
    print(f"Try GET /api/runs/{run_id}/metrics?name=loss")

if __name__ == "__main__":
    main()