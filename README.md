# ML Experiment Tracker (mini Weights & Biases)

A local-first ML experiment tracker that stores runs, params, and metrics in SQLite and shows them in a simple dashboard.

## MVP Goals
- Create runs
- Log params
- Log metrics over steps
- View runs + charts in a web dashboard

## Tech Stack
- Python, FastAPI
- SQLite
- Simple web UI (dashboard)

## Planned Repo Layout
- `server/` FastAPI app + DB
- `mltrack/` lightweight client SDK (later)
- `scripts/` demo training scripts

## Quickstart (coming soon)
1) Create venv  
2) Install deps  
3) Run server  
4) Run demo script to generate metrics