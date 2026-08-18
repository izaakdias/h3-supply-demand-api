"""FastAPI application for geospatial supply-demand snapshots."""

from fastapi import FastAPI

from .schemas import PredictRequest, SupplyDemandResponse
from .service import build_snapshot

app = FastAPI(
    title="H3 Supply & Demand API",
    version="0.1.0",
    description="Explainable synthetic mobility supply-demand snapshots by H3 cell.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/supply-demand/predict", response_model=SupplyDemandResponse)
def predict(request: PredictRequest) -> SupplyDemandResponse:
    return build_snapshot(request.latitude, request.longitude, request.resolution)
