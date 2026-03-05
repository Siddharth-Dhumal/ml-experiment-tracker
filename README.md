<h1 align="center">
  <br>
  🧪 ML Experiment Tracker
  <br>
</h1>

<p align="center">
  <b>A local-first, zero-cloud ML experiment tracking system — your own mini Weights & Biases.</b>
  <br>
  Track runs, log params & metrics, and visualize training curves, all from a clean REST API and web dashboard.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-local--first-003B57?style=flat-square&logo=sqlite&logoColor=white" />
  <img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Siddharth-Dhumal/ml-experiment-tracker/ci.yml?branch=main&style=flat-square&label=CI&logo=github-actions&logoColor=white" />
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" />
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#️-architecture">Architecture</a> •
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-api-reference">API Reference</a> •
  <a href="#-python-sdk">Python SDK</a> •
  <a href="#-development">Development</a>
</p>

---

## ✨ Features

| Capability | Details |
|---|---|
| 🏃 **Run Management** | Create, list, and update experiment runs with project/experiment scoping |
| 📋 **Hyperparameter Logging** | Upsert key–value params (any JSON-serializable type) per run |
| 📈 **Metric Tracking** | Log named metrics at every training step with timestamps |
| 🖥 **Web Dashboard** | Server-rendered HTML dashboard to browse runs and inspect metrics |
| 📊 **Interactive Charts** | Per-run metric charts powered by Chart.js with a live metric selector |
| 🌐 **REST API + Swagger** | Full OpenAPI docs at `/docs` — ready for curl, Postman, or any HTTP client |
| 🐍 **Lightweight Python SDK** | Drop-in `mltrack` client — one import, three method calls to track a training loop |
| 🗄 **SQLite Backend** | Zero-config, file-based persistence — no Docker, no external database |
| ✅ **CI Pipeline** | GitHub Actions workflow: install → lint (Ruff) → test (pytest + httpx) |

---

## 🏗️ Architecture

```
ml-experiment-tracker/
│
├── server/                  # FastAPI application
│   ├── main.py              # App factory, startup hooks, router registration
│   ├── api/
│   │   ├── runs.py          # CRUD endpoints for runs (POST / GET / PATCH)
│   │   └── logging.py       # Param upsert & metric logging endpoints
│   ├── db/
│   │   ├── models.py        # SQLAlchemy ORM: Run, Param, Metric
│   │   ├── base.py          # Declarative base
│   │   ├── session.py       # DB session factory & dependency
│   │   └── init_db.py       # DB initialisation on startup
│   ├── schemas/
│   │   ├── runs.py          # Pydantic models: RunCreate / RunRead / RunUpdate
│   │   └── logging.py       # Pydantic models: ParamItem / MetricItem / *Read
│   ├── ui/
│   │   └── pages.py         # Server-rendered HTML routes (/ui, /ui/runs/{id})
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS + Chart.js glue script
│
├── mltrack/                 # Lightweight Python SDK
│   ├── __init__.py          # Exports: Run
│   ├── run.py               # Run dataclass — create / log_params / log_metrics / finish / fail
│   └── client.py            # MLTrackClient — thin HTTP wrapper over requests
│
├── scripts/
│   └── demo_train.py        # End-to-end demo: creates a run, logs 20 steps of fake metrics
│
├── data/                    # Auto-created at runtime — holds mltrack.db
├── .github/workflows/ci.yml # GitHub Actions CI (Python 3.13, Ruff, pytest)
├── Makefile                 # Convenience targets: install / dev / test / lint / demo
└── requirements*.txt        # Runtime + dev dependencies
```

### Data Model

```
Run (id, project, experiment, name, status, started_at, ended_at)
 ├── Param (run_id, key, value)          ← upsert semantics (unique on run+key)
 └── Metric (run_id, name, value, step, timestamp)
```

A **Run** belongs to a `project` + `experiment` pair and transitions through states: `running` → `finished` | `failed`. Params are idempotent (upsert on key). Metrics are append-only, ordered by step.

---

## 🚀 Quickstart

### 1. Clone & install

```bash
git clone https://github.com/Siddharth-Dhumal/ml-experiment-tracker.git
cd ml-experiment-tracker

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt -r requirements-dev.txt
# or simply:
make install
```

### 2. Start the server

```bash
make dev
# Equivalent: python -m uvicorn server.main:app --reload --port 8000
```

The server auto-creates `data/mltrack.db` on first run.

### 3. Run the demo training script

Open a second terminal (with the venv activated):

```bash
make demo
# Equivalent: python -m scripts.demo_train
```

This creates a run named `demo-train` under project `demo / mnist`, logs hyperparameters, then simulates 20 training steps of `loss` and `acc` metrics.

### 4. Open the dashboard

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/ui` | Run list dashboard |
| `http://127.0.0.1:8000/ui/runs/{id}` | Per-run detail: params + metric chart |
| `http://127.0.0.1:8000/docs` | Interactive Swagger UI |
| `http://127.0.0.1:8000/health` | Health check endpoint |

---

## 🌐 API Reference

All endpoints are prefixed with `/api/runs`.

### Runs

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/runs` | Create a new run |
| `GET` | `/api/runs` | List all runs (optional `?status=running\|finished\|failed`) |
| `GET` | `/api/runs/{id}` | Get a single run |
| `PATCH` | `/api/runs/{id}` | Update run status (`running` → `finished` or `failed`) |

**Create a run:**
```bash
curl -s -X POST http://127.0.0.1:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{"project": "vision", "experiment": "resnet50", "name": "run-01"}'
```

```json
{
  "id": 1,
  "project": "vision",
  "experiment": "resnet50",
  "name": "run-01",
  "status": "running",
  "started_at": "2025-01-01T00:00:00",
  "ended_at": null
}
```

### Params

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/runs/{id}/params` | Upsert a list of key–value params |
| `GET` | `/api/runs/{id}/params` | List all params for a run |

```bash
curl -s -X POST http://127.0.0.1:8000/api/runs/1/params \
  -H "Content-Type: application/json" \
  -d '[{"key": "lr", "value": 0.001}, {"key": "batch_size", "value": 64}]'
```

### Metrics

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/runs/{id}/metrics` | Batch-log metric values at steps |
| `GET` | `/api/runs/{id}/metrics` | Query metrics (optional `?name=loss&limit=500`) |

```bash
curl -s -X POST http://127.0.0.1:8000/api/runs/1/metrics \
  -H "Content-Type: application/json" \
  -d '[{"name": "loss", "value": 0.42, "step": 10}]'
```

---

## 🐍 Python SDK

The `mltrack` package wraps the REST API with a clean, Pythonic interface. No configuration required — it talks to `http://127.0.0.1:8000` by default, or reads `MLTRACK_BASE_URL` from the environment.

```python
from mltrack import Run

# Create a run and log initial hyperparameters in one call
run = Run.create(
    project="vision",
    experiment="resnet50",
    name="baseline",
    params={
        "lr": 3e-4,
        "batch_size": 128,
        "optimizer": "adamw",
        "epochs": 50,
    },
)

# Inside your training loop
for epoch in range(50):
    train_loss, val_acc = ..., ...

    run.log_metrics({"train_loss": train_loss, "val_acc": val_acc}, step=epoch)

# Mark the run as complete
run.finish()   # or run.fail() on exception
```

### SDK at a glance

| Method | Signature | Description |
|---|---|---|
| `Run.create(...)` | `(project, experiment, name, *, params?, base_url?, timeout_s?)` → `Run` | Create run, optionally log params |
| `run.log_params(params)` | `Dict[str, Any]` → None | Upsert hyperparameters (idempotent) |
| `run.log_metrics(metrics, step=n)` | `Dict[str, float], int` → None | Append metric values at a step |
| `run.finish()` | — | Set status to `finished`, record `ended_at` |
| `run.fail()` | — | Set status to `failed`, record `ended_at` |

---

## 🛠 Development

### Makefile targets

```bash
make install   # pip-install runtime + dev dependencies
make dev       # start uvicorn with --reload on port 8000
make test      # run the full pytest suite
make lint      # run ruff linter
make demo      # fire the demo training script against a running server
```

### Running tests

```bash
pytest -q
```

Tests use `httpx`'s `TestClient` against an in-memory FastAPI app backed by a throwaway SQLite database (`data/test_mltrack.db`), so no server needs to be running.

**Test coverage:**

| Test | What it validates |
|---|---|
| `test_create_and_list_runs` | POST creates a run with `status=running`; GET returns it |
| `test_params_upsert` | Params are created; re-posting the same key updates the value |
| `test_metrics_log_and_filter` | Batch metric insert; `?name=` filter returns only matching rows |
| `test_finish_run_sets_ended_at` | PATCH to `finished` sets `ended_at` and persists the status |

### CI

Every push and pull request triggers the GitHub Actions pipeline:

1. **Install** — `pip install -r requirements.txt -r requirements-dev.txt`
2. **Lint** — `ruff check .`
3. **Test** — `pytest -q`

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **API Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/) |
| **ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) (Core + ORM) |
| **Database** | SQLite (file-based, zero-config) |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev/) |
| **Templating** | [Jinja2](https://jinja.palletsprojects.com/) |
| **Charting** | [Chart.js](https://www.chartjs.org/) (CDN) |
| **HTTP Client (SDK)** | [Requests](https://requests.readthedocs.io/) |
| **Testing** | [pytest](https://pytest.org/) + [httpx](https://www.python-httpx.org/) |
| **Linting** | [Ruff](https://docs.astral.sh/ruff/) |
| **CI** | GitHub Actions |

---

## 📄 License

MIT © [Siddharth Dhumal](https://github.com/Siddharth-Dhumal)