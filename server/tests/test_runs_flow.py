def test_create_and_list_runs(client):
    resp = client.post("/api/runs", json={"project": "demo", "experiment": "t", "name": "r1"})
    assert resp.status_code == 201
    run = resp.json()
    assert run["id"] >= 1
    assert run["status"] == "running"
    assert run["ended_at"] is None

    resp = client.get("/api/runs")
    assert resp.status_code == 200
    runs = resp.json()
    assert len(runs) == 1
    assert runs[0]["id"] == run["id"]


def test_params_upsert(client):
    run_id = client.post("/api/runs", json={"project": "demo", "experiment": "t", "name": "r1"}).json()["id"]

    resp = client.post(
        f"/api/runs/{run_id}/params",
        json=[{"key": "lr", "value": 0.001}, {"key": "batch_size", "value": 64}],
    )
    assert resp.status_code == 200
    params = resp.json()
    assert len(params) == 2

    resp = client.post(f"/api/runs/{run_id}/params", json=[{"key": "lr", "value": 0.01}])
    assert resp.status_code == 200

    resp = client.get(f"/api/runs/{run_id}/params")
    assert resp.status_code == 200
    params = {p["key"]: p["value"] for p in resp.json()}
    assert "lr" in params
    assert "0.01" in params["lr"]
    assert "batch_size" in params


def test_metrics_log_and_filter(client):
    run_id = client.post("/api/runs", json={"project": "demo", "experiment": "t", "name": "r1"}).json()["id"]

    resp = client.post(
        f"/api/runs/{run_id}/metrics",
        json=[
            {"name": "loss", "value": 1.0, "step": 0},
            {"name": "loss", "value": 0.8, "step": 1},
            {"name": "acc", "value": 0.5, "step": 0},
        ],
    )
    assert resp.status_code == 200
    assert resp.json()["inserted"] == 3

    resp = client.get(f"/api/runs/{run_id}/metrics?name=loss")
    assert resp.status_code == 200
    loss = resp.json()
    assert len(loss) == 2
    assert [m["step"] for m in loss] == [0, 1]


def test_finish_run_sets_ended_at(client):
    run = client.post("/api/runs", json={"project": "demo", "experiment": "t", "name": "r1"}).json()
    run_id = run["id"]

    resp = client.patch(f"/api/runs/{run_id}", json={"status": "finished"})
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["status"] == "finished"
    assert updated["ended_at"] is not None