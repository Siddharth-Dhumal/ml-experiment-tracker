import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

os.environ["MLTRACK_DB_URL"] = "sqlite:///./data/test_mltrack.db"

from server.main import app
from server.db.session import engine

TEST_DB = Path("data/test_mltrack.db")

@pytest.fixture()
def client():
    Path("data").mkdir(exist_ok=True)

    engine.dispose()

    for suffix in ["", "-wal", "-shm"]:
        p = Path(str(TEST_DB) + suffix)
        if p.exists():
            p.unlink()

    with TestClient(app) as c:
        yield c

    engine.dispose()