import asyncio
import logging
from unittest.mock import patch

import pytest
from fastapi import FastAPI, HTTPException


@pytest.fixture
def app():
    app = FastAPI()

    @app.get("/")
    async def read_root():
        return {"message": "Hello World"}

    @app.get("/slow")
    async def slow_endpoint():
        await asyncio.sleep(0.1)
        return {"message": "Slow response"}

    @app.get("/error")
    async def error_endpoint():
        raise HTTPException(status_code=404, detail="Not found")

    @app.get("/server-error")
    async def server_error_endpoint():
        raise Exception("Internal server error")

    @app.post("/create")
    async def create_endpoint():
        return {"message": "Created"}

    @app.put("/update")
    async def update_endpoint():
        return {"message": "Updated"}

    @app.delete("/delete")
    async def delete_endpoint():
        return {"message": "Deleted"}

    return app


@pytest.fixture(autouse=True)
def reset_uvicorn_logging():
    yield

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.disabled = False
    uvicorn_access_logger.propagate = True

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.WARNING)


@pytest.fixture
def mock_datetime():
    with patch("logging_middleware.middleware.datetime") as mock_dt:
        mock_dt.now.return_value.strftime.return_value = "2023-01-01 12:00:00.000000"
        yield mock_dt


@pytest.fixture
def mock_time():
    with patch("logging_middleware.middleware.time.perf_counter") as mock_perf:
        mock_perf.side_effect = [0.0, 0.01]  # 10ms
        yield mock_perf
