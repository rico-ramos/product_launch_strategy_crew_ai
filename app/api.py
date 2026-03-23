from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import LaunchRequest, LaunchResponse
from app.services.orchestration import run_launch_strategy
from app.services.storage import load_run

app = FastAPI(title="Launch Strategy AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/launch-strategy/run", response_model=LaunchResponse)
def run_strategy(request: LaunchRequest):
    try:
        return run_launch_strategy(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/v1/launch-strategy/runs/{run_id}")
def get_run(run_id: str):
    try:
        return load_run(run_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Run not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
